from odoo import models, fields, api


class PhongBan(models.Model):
    _name = 'phong_ban'
    _description = 'Bảng chứa thông tin phòng ban'
    _order = 'ma_phong_ban'

    ma_phong_ban = fields.Char("Mã phòng ban", required=True)
    tem_phong_ban = fields.Date("Tên phòng ban")
