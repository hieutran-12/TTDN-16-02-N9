# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HoaDonMua(models.Model):
    _name = 'hoa_don_mua'
    _description = 'Hóa đơn mua'
    _order = 'ngay_hoa_don desc'

    name = fields.Char('Số hóa đơn', required=True, copy=False, readonly=True, default='/')
    ma_hoa_don = fields.Char('Mã hóa đơn NCC')
    ngay_hoa_don = fields.Date('Ngày hóa đơn', required=True, default=fields.Date.context_today)
    nha_cung_cap_id = fields.Many2one('res.partner', string='Nhà cung cấp', required=True)
    tong_tien = fields.Monetary('Tổng tiền', compute='_compute_tong_tien', store=True)
    tien_thue = fields.Monetary('Tiền thuế', compute='_compute_tong_tien', store=True)
    tong_thanh_toan = fields.Monetary('Tổng thanh toán', compute='_compute_tong_tien', store=True)
    currency_id = fields.Many2one('res.currency', string='Tiền tệ', default=lambda self: self.env.company.currency_id)
    ghi_chu = fields.Text('Ghi chú')
    state = fields.Selection([
        ('nhap', 'Nháp'),
        ('xac_nhan', 'Xác nhận'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy', 'Hủy'),
    ], string='Trạng thái', default='nhap')
    chi_tiet_ids = fields.One2many('chi_tiet_hoa_don_mua', 'hoa_don_mua_id', string='Chi tiết hóa đơn')
    nguoi_mua_id = fields.Many2one('res.users', string='Người mua', default=lambda self: self.env.user)
    # nhan_vien_id = fields.Many2one('hr.employee', string='Nhân viên thực hiện', help='Nhân viên kế toán hoặc người phụ trách đơn hàng')  # REMOVED: hr module not installed
    but_toan_id = fields.Many2one('but_toan_ke_toan', string='Bút toán mua', readonly=True)
    cong_no_mua_id = fields.Many2one('cong_no_mua', string='Công nợ mua', readonly=True)
    
    # ==================== TÀI SẢN CỐ ĐỊNH ====================
    co_tai_san = fields.Boolean(
        'Có phát sinh tài sản',
        default=False,
        help='Đánh dấu nếu hóa đơn này có phát sinh tài sản cố định'
    )
    asset_status = fields.Selection([
        ('pending', 'Chờ tạo'),
        ('created', 'Đã tạo'),
    ], string='Trạng thái tài sản', default='pending', readonly=True)
    ma_tai_san_created = fields.Char(
        string='Mã tài sản tạo từ HĐ',
        readonly=True,
        help='Mã tài sản tự động sinh từ hóa đơn này'
    )

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('hoa_don_mua') or '/'
        return super(HoaDonMua, self).create(vals)

    @api.depends('chi_tiet_ids.thanh_tien', 'chi_tiet_ids.tien_thue', 'chi_tiet_ids.tong_cong')
    def _compute_tong_tien(self):
        for rec in self:
            rec.tong_tien = sum(line.thanh_tien for line in rec.chi_tiet_ids)
            rec.tien_thue = sum(line.tien_thue for line in rec.chi_tiet_ids)
            rec.tong_thanh_toan = sum(line.tong_cong for line in rec.chi_tiet_ids)

    def action_xac_nhan(self):
        """Xác nhận hóa đơn và tự động tạo:
        1. Bút toán mua hàng
        2. Công nợ
        3. Đánh dấu trạng thái tài sản nếu có phát sinh
        """
        for rec in self:
            if rec.state != 'nhap':
                raise ValidationError(_('Chỉ có thể xác nhận hóa đơn nháp!'))
            
            # BƯỚC 1: Tạo bút toán mua
            but_toan_vals = {
                'loai_but_toan': 'mua_hang',
                'dien_giai': f'Mua hàng từ {rec.nha_cung_cap_id.name} - {rec.name}',
                'chung_tu_lien_quan': f'hoa_don_mua,{rec.id}',
                'ngay_but_toan': rec.ngay_hoa_don,
            }
            chi_tiet_lines = []
            
            # Debit: Tài sản/Chi phí + Thuế GTGT (nếu có)
            for line in rec.chi_tiet_ids:
                # Nợ TK tài sản/chi phí
                tk_no = line.tai_khoan_id if line.tai_khoan_id else (
                    self.env.ref('tai_chinh_ke_toan.tai_khoan_tai_san') if line.la_tai_san 
                    else self.env.ref('tai_chinh_ke_toan.tai_khoan_chi_phi')
                )
                chi_tiet_lines.append((0, 0, {
                    'tai_khoan_id': tk_no.id,
                    'dien_giai': line.ten_san_pham,
                    'tien_no': line.thanh_tien,
                    'tien_co': 0,
                    'doi_tac_id': rec.nha_cung_cap_id.id,
                }))
                
                # Nếu có thuế GTGT đầu vào
                if line.tien_thue > 0:
                    chi_tiet_lines.append((0, 0, {
                        'tai_khoan_id': self.env.ref('tai_chinh_ke_toan.tai_khoan_1331').id,  # TK 1331
                        'dien_giai': f'Thuế GTGT đầu vào - {line.ten_san_pham}',
                        'tien_no': line.tien_thue,
                        'tien_co': 0,
                        'doi_tac_id': rec.nha_cung_cap_id.id,
                    }))
            
            # Credit: Nợ phải trả (TK 331)
            chi_tiet_lines.append((0, 0, {
                'tai_khoan_id': self.env.ref('tai_chinh_ke_toan.tai_khoan_no_phai_tra').id,
                'dien_giai': f'Phải trả {rec.nha_cung_cap_id.name}',
                'tien_no': 0,
                'tien_co': rec.tong_thanh_toan,
                'doi_tac_id': rec.nha_cung_cap_id.id,
            }))
            
            but_toan_vals['chi_tiet_ids'] = chi_tiet_lines
            but_toan = self.env['but_toan_ke_toan'].create(but_toan_vals)
            rec.but_toan_id = but_toan.id
            
            # BƯỚC 2: Tạo công nợ
            cong_no = self.env['cong_no_mua'].create({
                'hoa_don_mua_id': rec.id,
                'nha_cung_cap_id': rec.nha_cung_cap_id.id,
                'so_tien_goc': rec.tong_thanh_toan,
                'han_thanh_toan': rec.ngay_hoa_don,
            })
            rec.cong_no_mua_id = cong_no.id
            
            # BƯỚC 3: Ghi sổ bút toán
            but_toan.action_ghi_so()
            
            # BƯỚC 4: Cập nhật trạng thái nếu có phát sinh tài sản
            if rec.co_tai_san:
                rec.asset_status = 'pending'
            
            rec.state = 'xac_nhan'

    def action_hoan_thanh(self):
        for rec in self:
            rec.state = 'hoan_thanh'
    
    def action_tao_tai_san(self):
        """Tạo tài sản từ hóa đơn mua - gọi từ QLTS pending view"""
        self.ensure_one()
        
        if not self.co_tai_san:
            raise ValidationError(_('Hóa đơn không được đánh dấu "Có phát sinh tài sản"!'))
        
        if self.asset_status == 'created':
            raise ValidationError(_('Tài sản từ hóa đơn này đã được tạo rồi!'))
        
        # Gọi method từ tai_san model để tạo tài sản
        return self.env['tai_san'].action_tao_tai_san_tu_hoa_don(self.id)

    def action_huy(self):
        for rec in self:
            # Hủy bút toán
            if rec.but_toan_id:
                rec.but_toan_id.action_huy_ghi_so()
                rec.but_toan_id.unlink()
            
            # Xóa công nợ
            if rec.cong_no_mua_id:
                rec.cong_no_mua_id.unlink()
            
            rec.state = 'huy'