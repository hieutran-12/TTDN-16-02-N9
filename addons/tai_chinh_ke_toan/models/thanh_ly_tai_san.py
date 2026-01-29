# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ThanhLyTaiSan(models.Model):
    _name = 'thanh_ly_tai_san'
    _description = 'Quản lý thanh lý tài sản cố định'
    _order = 'ma_thanh_ly desc'
    _sql_constraints = [
        ('ma_thanh_ly_unique', 'unique(ma_thanh_ly)', 'Mã thanh lý phải là duy nhất!')
    ]

    # ==================== THÔNG TIN CƠ BẢN ====================
    ma_thanh_ly = fields.Char("Mã thanh lý", copy=False, readonly=True, default="New")
    ngay_thanh_ly = fields.Date("Ngày thanh lý", required=True, default=fields.Date.today)
    
    # THAM CHIẾU TÀI SẢN (STRING - KHÔNG PHẢI MANY2ONE)
    ma_tai_san = fields.Char(
        string="Mã tài sản",
        required=True,
        help="Mã tham chiếu đến tài sản từ module QLTS (VD: TS-00001)"
    )
    ten_tai_san = fields.Char("Tên tài sản", required=True)
    
    gia_tri_thanh_ly = fields.Monetary(
        "Giá trị thanh lý", required=True, currency_field='currency_id',
        help="Số tiền thu được từ thanh lý"
    )
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    
    # Thông tin tài sản (nhập tay từ QLTS)
    nguyen_gia = fields.Monetary("Nguyên giá", currency_field='currency_id', required=True)
    khau_hao_luy_ke = fields.Monetary("Khấu hao lũy kế", currency_field='currency_id', required=True)
    gia_tri_con_lai = fields.Monetary("Giá trị còn lại", compute='_compute_gia_tri_con_lai', store=True, currency_field='currency_id')
    
    # Lãi/lỗ thanh lý
    chenh_lech_thanh_ly = fields.Monetary(
        "Chênh lệch thanh lý", compute='_compute_chenh_lech', store=True,
        currency_field='currency_id', help="Dương = Lãi, Âm = Lỗ"
    )
    
    # Trạng thái
    TRANG_THAI = [
        ('draft', 'Nháp'),
        ('confirmed', 'Đã xác nhận'),
        ('done', 'Hoàn thành'),
        ('cancelled', 'Đã hủy'),
    ]
    trang_thai = fields.Selection(TRANG_THAI, string="Trạng thái", default='draft', required=True, tracking=True)
    
    ly_do = fields.Text("Lý do thanh lý")
    nguoi_xu_ly_id = fields.Many2one('res.users', string="Người xử lý", required=True, default=lambda self: self.env.user)
    
    # Liên kết bút toán
    but_toan_id = fields.Many2one('but_toan_ke_toan', string='Bút toán thanh lý', readonly=True, ondelete='set null')
    
    # Tài khoản kế toán
    tai_khoan_nguyen_gia_id = fields.Many2one('tai_khoan_ke_toan', string='TK Nguyên giá (211/213)', required=True)
    tai_khoan_hao_mon_id = fields.Many2one('tai_khoan_ke_toan', string='TK Hao mòn (214)', required=True)

    # ==================== COMPUTED ====================
    @api.depends('nguyen_gia', 'khau_hao_luy_ke')
    def _compute_gia_tri_con_lai(self):
        for rec in self:
            rec.gia_tri_con_lai = rec.nguyen_gia - rec.khau_hao_luy_ke

    @api.depends('gia_tri_thanh_ly', 'gia_tri_con_lai')
    def _compute_chenh_lech(self):
        for rec in self:
            rec.chenh_lech_thanh_ly = rec.gia_tri_thanh_ly - rec.gia_tri_con_lai

    # ==================== CRUD ====================
    @api.model
    def create(self, vals):
        # Auto generate mã
        if vals.get('ma_thanh_ly', 'New') == 'New':
            last_record = self.search([], order='ma_thanh_ly desc', limit=1)
            if last_record and last_record.ma_thanh_ly.startswith('TL-'):
                last_number = int(last_record.ma_thanh_ly.split('-')[1])
                new_number = last_number + 1
            else:
                new_number = 1
            vals['ma_thanh_ly'] = f'TL-{new_number:05d}'
        
        return super(ThanhLyTaiSan, self).create(vals)

    # ==================== ACTIONS ====================
    def action_confirm(self):
        """Button: Xác nhận phiếu thanh lý"""
        self.ensure_one()
        if self.trang_thai == 'draft':
            self.trang_thai = 'confirmed'
        else:
            raise ValidationError("Chỉ có thể xác nhận phiếu ở trạng thái Nháp!")

    def action_done(self):
        """Button: Hoàn thành thanh lý và tạo bút toán"""
        self.ensure_one()
        
        if self.trang_thai != 'confirmed':
            raise ValidationError("Phiếu cần được xác nhận trước khi hoàn thành!")
        
        # Tạo bút toán thanh lý
        if not self.but_toan_id:
            self._tao_but_toan_thanh_ly()
        
        # GỬI THÔNG BÁO ĐẾN MODULE QLTS
        self._gui_thong_bao_thanh_ly_den_qlts()
        
        # Hoàn thành
        self.trang_thai = 'done'

    def action_cancel(self):
        """Button: Hủy phiếu thanh lý"""
        self.ensure_one()
        
        if self.trang_thai in ('draft', 'confirmed'):
            # Hủy bút toán nếu có
            if self.but_toan_id:
                self.but_toan_id.action_huy_ghi_so()
                self.but_toan_id.unlink()
            
            self.trang_thai = 'cancelled'
        else:
            raise ValidationError("Không thể hủy phiếu đã hoàn thành!")

    # ==================== BUSINESS LOGIC ====================
    def _tao_but_toan_thanh_ly(self):
        """
        Tạo bút toán thanh lý TSCĐ (3-4 dòng):
        1. Nợ TK 214 (Xóa hao mòn lũy kế)
        2. Nợ TK 111 (Thu tiền thanh lý)
        3. Có TK 211 (Xóa nguyên giá)
        4. (Nếu có lãi/lỗ) Nợ/Có TK 811/711
        """
        self.ensure_one()
        
        chi_tiet_lines = []
        
        # Dòng 1: Xóa hao mòn lũy kế (Nợ TK 214)
        if self.khau_hao_luy_ke > 0:
            chi_tiet_lines.append((0, 0, {
                'tai_khoan_id': self.tai_khoan_hao_mon_id.id,
                'tien_no': self.khau_hao_luy_ke,
                'tien_co': 0,
                'dien_giai': f'Xóa hao mòn lũy kế - {self.ten_tai_san}',
            }))
        
        # Dòng 2: Thu tiền thanh lý (Nợ TK 111)
        if self.gia_tri_thanh_ly > 0:
            chi_tiet_lines.append((0, 0, {
                'tai_khoan_id': self.env.ref('tai_chinh_ke_toan.tai_khoan_111').id,  # TK 111
                'tien_no': self.gia_tri_thanh_ly,
                'tien_co': 0,
                'dien_giai': f'Thu tiền thanh lý - {self.ten_tai_san}',
            }))
        
        # Dòng 3: Xóa nguyên giá (Có TK 211)
        chi_tiet_lines.append((0, 0, {
            'tai_khoan_id': self.tai_khoan_nguyen_gia_id.id,
            'tien_no': 0,
            'tien_co': self.nguyen_gia,
            'dien_giai': f'Xóa nguyên giá TSCĐ - {self.ten_tai_san}',
        }))
        
        # Dòng 4: Ghi nhận lãi/lỗ thanh lý (nếu có)
        if self.chenh_lech_thanh_ly != 0:
            if self.chenh_lech_thanh_ly > 0:
                # Lãi thanh lý: Có TK 711
                chi_tiet_lines.append((0, 0, {
                    'tai_khoan_id': self.env.ref('tai_chinh_ke_toan.tai_khoan_711').id,
                    'tien_no': 0,
                    'tien_co': abs(self.chenh_lech_thanh_ly),
                    'dien_giai': f'Lãi thanh lý TSCĐ - {self.ten_tai_san}',
                }))
            else:
                # Lỗ thanh lý: Nợ TK 811
                chi_tiet_lines.append((0, 0, {
                    'tai_khoan_id': self.env.ref('tai_chinh_ke_toan.tai_khoan_811').id,
                    'tien_no': abs(self.chenh_lech_thanh_ly),
                    'tien_co': 0,
                    'dien_giai': f'Lỗ thanh lý TSCĐ - {self.ten_tai_san}',
                }))
        
        # Tạo bút toán
        but_toan = self.env['but_toan_ke_toan'].create({
            'ngay_but_toan': self.ngay_thanh_ly,
            'dien_giai': f'Thanh lý tài sản {self.ten_tai_san}',
            'loai_but_toan': 'thanh_ly',
            'chi_tiet_ids': chi_tiet_lines,
        })
        
        # Ghi sổ
        but_toan.action_ghi_so()
        
        # Link bút toán
        self.but_toan_id = but_toan.id
        
        return but_toan

    def _gui_thong_bao_thanh_ly_den_qlts(self):
        """
        GỬI THÔNG BÁO THANH LÝ ĐẾN MODULE QLTS
        Cập nhật field ma_phieu_thanh_ly và ngay_thanh_ly trong bảng tai_san
        """
        self.ensure_one()
        
        # Tìm tài sản theo mã (STRING)
        tai_san = self.env['tai_san'].search([('ma_tai_san', '=', self.ma_tai_san)], limit=1)
        
        if tai_san:
            # Cập nhật thông tin thanh lý
            tai_san.write({
                'ma_phieu_thanh_ly': self.ma_thanh_ly,
                'ngay_thanh_ly': self.ngay_thanh_ly,
                'trang_thai': 'DaThanhLy',  # Cập nhật trạng thái
            })
        else:
            raise ValidationError(f"Không tìm thấy tài sản có mã '{self.ma_tai_san}' trong hệ thống QLTS!")