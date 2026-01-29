from odoo import models, fields

class Thue(models.Model):
    _name = 'thue'
    _description = 'Thuế suất'
    _order = 'ty_le_thue desc'

    ten_thue = fields.Char('Tên thuế', required=True)
    ty_le_thue = fields.Float('Tỷ lệ thuế (%)', required=True)
    tai_khoan_thue_id = fields.Many2one('tai_khoan_ke_toan', string='Tài khoản thuế')
    active = fields.Boolean('Kích hoạt', default=True)
