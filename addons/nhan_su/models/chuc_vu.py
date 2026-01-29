from odoo import models, fields, api


class ChucVu(models.Model):
    _name = 'chuc_vu'
    _description = 'Bảng chứa thông tin chức vụ'
    _order = 'ma_chuc_vu'

    ma_chuc_vu = fields.Char("Mã chức vụ", required=True, store=True)
    ten_chuc_vu = fields.Text("Tên chức vụ")
    phong_ban_id = fields.Many2one(comodel_name='phong_ban', string='Phòng ban', required=True)