# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ChiTietHoaDonMua(models.Model):
    _name = 'chi_tiet_hoa_don_mua'
    _description = 'Chi tiết hóa đơn mua'
    _order = 'hoa_don_mua_id, id'

    hoa_don_mua_id = fields.Many2one('hoa_don_mua', string='Hóa đơn mua', required=True, ondelete='cascade')
    # product_id = fields.Many2one('product.product', string='Sản phẩm')  # REMOVED: product module not in use
    ten_san_pham = fields.Char('Tên sản phẩm', required=True)
    so_luong = fields.Float('Số lượng', default=1)
    don_gia = fields.Monetary('Đơn giá')
    thue_id = fields.Many2one('thue', string='Thuế suất')
    thanh_tien = fields.Monetary('Thành tiền', compute='_compute_thanh_tien', store=True)
    tien_thue = fields.Monetary('Tiền thuế', compute='_compute_thanh_tien', store=True)
    tong_cong = fields.Monetary('Tổng cộng', compute='_compute_thanh_tien', store=True)
    tai_khoan_id = fields.Many2one('tai_khoan_ke_toan', string='Tài khoản kế toán')
    la_tai_san = fields.Boolean('Là tài sản cố định', default=False)
    currency_id = fields.Many2one('res.currency', related='hoa_don_mua_id.currency_id', store=True, readonly=True)

    # REMOVED: product module not in use
    # @api.onchange('product_id')
    # def _onchange_product_id(self):
    #     if self.product_id:
    #         self.ten_san_pham = self.product_id.name
    #         self.don_gia = self.product_id.standard_price

    @api.depends('so_luong', 'don_gia', 'thue_id')
    def _compute_thanh_tien(self):
        for rec in self:
            rec.thanh_tien = rec.so_luong * rec.don_gia
            rec.tien_thue = rec.thanh_tien * (rec.thue_id.ty_le_thue/100) if rec.thue_id else 0
            rec.tong_cong = rec.thanh_tien + rec.tien_thue