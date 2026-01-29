# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class KhauHaoTaiSan(models.Model):
    _name = 'khau_hao_tai_san'
    _description = 'Khấu hao tài sản cố định'
    _order = 'nam desc, thang desc, ngay_khau_hao desc'
    _sql_constraints = [
        ('unique_tai_san_thang_nam', 'unique(ma_tai_san, thang, nam)', 
         'Tài sản đã có bản ghi khấu hao trong tháng này!')
    ]

    # ==================== THÔNG TIN CƠ BẢN ====================
    ma_khau_hao = fields.Char("Mã khấu hao", copy=False, readonly=True, default="New")
    
    # THAM CHIẾU TÀI SẢN (CHAR - MÃ TÀI SẢN, KHÔNG BACKLINK)
    ma_tai_san = fields.Char(
        "Mã tài sản",
        required=True,
        help="Mã tài sản từ module quản lý tài sản (lưu mã, không backlink)"
    )
    
    # Thời gian
    thang = fields.Integer("Tháng", required=True, default=lambda self: fields.Date.today().month)
    nam = fields.Integer("Năm", required=True, default=lambda self: fields.Date.today().year)
    ngay_khau_hao = fields.Date("Ngày ghi nhận", required=True, default=fields.Date.today)
    
    # Phương pháp
    phuong_phap_khau_hao = fields.Selection([
        ('duong_thang', 'Khấu hao đường thẳng'),
        ('so_du_giam_dan', 'Khấu hao số dư giảm dần'),
        ('theo_san_luong', 'Khấu hao theo sản lượng'),
    ], string="Phương pháp", required=True, default='duong_thang')
    
    # Giá trị
    nguyen_gia = fields.Monetary("Nguyên giá", currency_field='currency_id')
    gia_tri_truoc_khau_hao = fields.Monetary(
        "Giá trị trước KH", currency_field='currency_id',
        help="Giá trị còn lại trước khi khấu hao tháng này"
    )
    gia_tri_khau_hao = fields.Monetary(
        "Giá trị khấu hao", required=True, currency_field='currency_id',
        help="Số tiền khấu hao trong tháng này"
    )
    gia_tri_con_lai = fields.Monetary(
        "Giá trị còn lại", compute='_compute_gia_tri_con_lai', store=True,
        currency_field='currency_id'
    )
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('du_kien', 'Dự kiến'),
        ('da_ghi_nhan', 'Đã ghi nhận'),
        ('huy', 'Hủy'),
    ], string="Trạng thái", default='du_kien', required=True)
    
    ghi_chu = fields.Text("Ghi chú")
    
    # Liên kết bút toán
    but_toan_id = fields.Many2one('but_toan_ke_toan', string='Bút toán', readonly=True, ondelete='set null')
    
    # Tài khoản kế toán
    tai_khoan_nguyen_gia_id = fields.Many2one('tai_khoan_ke_toan', string='TK Nguyên giá (211/213)', required=True)
    tai_khoan_hao_mon_id = fields.Many2one('tai_khoan_ke_toan', string='TK Hao mòn (214)', required=True)
    tai_khoan_chi_phi_id = fields.Many2one('tai_khoan_ke_toan', string='TK Chi phí KH (627/642)', required=True)

    # ==================== COMPUTED ====================
    @api.depends('gia_tri_truoc_khau_hao', 'gia_tri_khau_hao')
    def _compute_gia_tri_con_lai(self):
        for rec in self:
            rec.gia_tri_con_lai = rec.gia_tri_truoc_khau_hao - rec.gia_tri_khau_hao

    # ==================== CRUD ====================
    @api.model
    def create(self, vals):
        # Auto generate mã
        if vals.get('ma_khau_hao', 'New') == 'New':
            last_record = self.search([], order='ma_khau_hao desc', limit=1)
            if last_record and last_record.ma_khau_hao.startswith('KH-'):
                try:
                    last_number = int(last_record.ma_khau_hao.split('-')[1])
                    new_number = last_number + 1
                except (ValueError, IndexError):
                    new_number = 1
            else:
                new_number = 1
            vals['ma_khau_hao'] = f'KH-{new_number:05d}'
        
        record = super(KhauHaoTaiSan, self).create(vals)
        
        # Tự động sinh bút toán khi tạo (nếu trạng thái = da_ghi_nhan)
        if record.trang_thai == 'da_ghi_nhan' and not record.but_toan_id:
            record._tao_but_toan_khau_hao()
        
        return record

    def write(self, vals):
        res = super(KhauHaoTaiSan, self).write(vals)
        
        # Nếu chuyển sang 'da_ghi_nhan' và chưa có bút toán → Tạo bút toán
        if vals.get('trang_thai') == 'da_ghi_nhan':
            for rec in self:
                if not rec.but_toan_id:
                    rec._tao_but_toan_khau_hao()
        
        return res

    # ==================== BUSINESS LOGIC ====================
    def _tao_but_toan_khau_hao(self):
        """Tự động tạo bút toán khấu hao: Nợ 627/642 - Có 214"""
        self.ensure_one()
        
        if self.gia_tri_khau_hao <= 0:
            raise ValidationError("Giá trị khấu hao phải lớn hơn 0!")
        
        # Tạo bút toán
        but_toan = self.env['but_toan_ke_toan'].create({
            'ngay_but_toan': self.ngay_khau_hao,
            'dien_giai': f'Khấu hao tháng {self.thang}/{self.nam} - {self.ten_tai_san}',
            'loai_but_toan': 'khau_hao',
            'chi_tiet_ids': [
                # Nợ TK Chi phí khấu hao (627/642)
                (0, 0, {
                    'tai_khoan_id': self.tai_khoan_chi_phi_id.id,
                    'tien_no': self.gia_tri_khau_hao,
                    'tien_co': 0,
                    'dien_giai': f'Chi phí khấu hao {self.ten_tai_san}',
                }),
                # Có TK Hao mòn lũy kế (214)
                (0, 0, {
                    'tai_khoan_id': self.tai_khoan_hao_mon_id.id,
                    'tien_no': 0,
                    'tien_co': self.gia_tri_khau_hao,
                    'dien_giai': f'Hao mòn lũy kế {self.ten_tai_san}',
                })
            ]
        })
        
        # Ghi sổ luôn
        but_toan.action_ghi_so()
        
        # Link bút toán
        self.but_toan_id = but_toan.id
        
        return but_toan

    def action_xac_nhan(self):
        """Button: Xác nhận khấu hao"""
        for rec in self:
            if rec.trang_thai != 'du_kien':
                raise ValidationError("Chỉ có thể xác nhận khấu hao ở trạng thái 'Dự kiến'!")
            
            rec.trang_thai = 'da_ghi_nhan'
            
            # Tạo bút toán nếu chưa có
            if not rec.but_toan_id:
                rec._tao_but_toan_khau_hao()

    def action_huy(self):
        """Button: Hủy khấu hao"""
        for rec in self:
            if rec.trang_thai == 'da_ghi_nhan':
                # Hủy bút toán nếu có
                if rec.but_toan_id:
                    rec.but_toan_id.action_huy_ghi_so()
                    rec.but_toan_id.unlink()
            
            rec.trang_thai = 'huy'