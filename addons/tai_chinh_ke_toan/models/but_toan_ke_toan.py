# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ButToanKeToan(models.Model):
    _name = 'but_toan_ke_toan'
    _description = 'Bút toán kế toán'
    _order = 'ngay_but_toan desc'

    name = fields.Char('Số bút toán', required=True, copy=False, readonly=True, default='/')
    ngay_but_toan = fields.Date('Ngày bút toán', required=True, default=fields.Date.context_today)
    dien_giai = fields.Text('Diễn giải', required=True)
    tong_tien_no = fields.Monetary('Tổng Nợ', compute='_compute_tong_tien', store=True)
    tong_tien_co = fields.Monetary('Tổng Có', compute='_compute_tong_tien', store=True)
    chi_tiet_ids = fields.One2many('chi_tiet_but_toan', 'but_toan_id', string='Chi tiết bút toán')
    state = fields.Selection([
        ('nhap', 'Nháp'),
        ('da_ghi_so', 'Đã ghi sổ'),
    ], string='Trạng thái', default='nhap')
    nguoi_tao_id = fields.Many2one('res.users', string='Người tạo', default=lambda self: self.env.user)
    loai_but_toan = fields.Selection([
        ('thu_tien', 'Thu tiền'),
        ('chi_tien', 'Chi tiền'),
        ('mua_hang', 'Mua hàng'),
        ('ban_hang', 'Bán hàng'),
        ('khau_hao', 'Khấu hao'),
        ('thanh_ly', 'Thanh lý'),
        ('khac', 'Khác'),
    ], string='Loại bút toán', required=True)
    chung_tu_lien_quan = fields.Reference([
        ('hoa_don_mua', 'Hóa đơn mua'),
    ], string='Chứng từ liên quan')
    currency_id = fields.Many2one('res.currency', string='Tiền tệ', default=lambda self: self.env.company.currency_id)

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('but_toan_ke_toan') or '/'
        return super(ButToanKeToan, self).create(vals)

    @api.depends('chi_tiet_ids.tien_no', 'chi_tiet_ids.tien_co')
    def _compute_tong_tien(self):
        for rec in self:
            rec.tong_tien_no = sum(line.tien_no for line in rec.chi_tiet_ids)
            rec.tong_tien_co = sum(line.tien_co for line in rec.chi_tiet_ids)

    @api.constrains('chi_tiet_ids')
    def _check_can_bang_no_co(self):
        for rec in self:
            if rec.state == 'da_ghi_so' and rec.tong_tien_no != rec.tong_tien_co:
                raise ValidationError(_('Bút toán không cân bằng Nợ/Có!'))

    def action_ghi_so(self):
        for rec in self:
            if rec.tong_tien_no != rec.tong_tien_co:
                raise ValidationError(_('Bút toán không cân bằng Nợ/Có!'))
            rec.state = 'da_ghi_so'

    def action_huy_ghi_so(self):
        for rec in self:
            rec.state = 'nhap'