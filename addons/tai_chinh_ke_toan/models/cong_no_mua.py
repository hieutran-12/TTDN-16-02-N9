from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class CongNoMua(models.Model):
    _name = 'cong_no_mua'
    _description = 'Công nợ mua'
    _order = 'han_thanh_toan asc'

    hoa_don_mua_id = fields.Many2one('hoa_don_mua', string='Hóa đơn mua', required=True, ondelete='cascade')
    nha_cung_cap_id = fields.Many2one('res.partner', related='hoa_don_mua_id.nha_cung_cap_id', store=True)
    so_tien_goc = fields.Monetary('Số tiền gốc')
    so_tien_con_lai = fields.Monetary('Số tiền còn lại', compute='_compute_tien_con_lai', store=True)
    han_thanh_toan = fields.Date('Hạn thanh toán')
    state = fields.Selection([
        ('co_cong_no', 'Có công nợ'),
        ('da_thanh_toan', 'Đã thanh toán'),
    ], string='Trạng thái', default='co_cong_no')
    chi_tiet_thanh_toan = fields.One2many('chi_tiet_thanh_toan_no', 'cong_no_mua_id', string='Chi tiết thanh toán')
    currency_id = fields.Many2one('res.currency', related='hoa_don_mua_id.currency_id', store=True)

    @api.depends('chi_tiet_thanh_toan.so_tien_thanh_toan')
    def _compute_tien_con_lai(self):
        for rec in self:
            tien_da_thanh_toan = sum(line.so_tien_thanh_toan for line in rec.chi_tiet_thanh_toan)
            rec.so_tien_con_lai = rec.so_tien_goc - tien_da_thanh_toan
            if rec.so_tien_con_lai == 0:
                rec.state = 'da_thanh_toan'
            else:
                rec.state = 'co_cong_no'

    @api.model
    def create(self, vals):
        if 'so_tien_goc' not in vals and 'hoa_don_mua_id' in vals:
            hoa_don = self.env['hoa_don_mua'].browse(vals['hoa_don_mua_id'])
            vals['so_tien_goc'] = hoa_don.tong_thanh_toan
        return super(CongNoMua, self).create(vals)


class ChiTietThanhToanNo(models.Model):
    _name = 'chi_tiet_thanh_toan_no'
    _description = 'Chi tiết thanh toán công nợ'

    cong_no_mua_id = fields.Many2one('cong_no_mua', string='Công nợ mua', required=True, ondelete='cascade')
    ngay_thanh_toan = fields.Date('Ngày thanh toán', default=fields.Date.context_today)
    so_tien_thanh_toan = fields.Monetary('Số tiền thanh toán')
    phuong_thuc_thanh_toan = fields.Selection([
        ('tien_mat', 'Tiền mặt'),
        ('chuyen_khoan', 'Chuyển khoản'),
        ('sek', 'Séc'),
        ('khac', 'Khác'),
    ], string='Phương thức thanh toán')
    but_toan_id = fields.Many2one('but_toan_ke_toan', string='Bút toán liên quan')
    currency_id = fields.Many2one('res.currency', related='cong_no_mua_id.currency_id', store=True)
