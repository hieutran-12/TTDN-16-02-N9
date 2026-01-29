from odoo import models, fields, api


class PhongBan(models.Model):
    _name = 'phong_ban'
    _description = 'Bảng chứa thông tin phòng ban'
    _order = 'ma_phong_ban'
    _rec_name = 'ten_phong_ban'

    ma_phong_ban = fields.Char("Mã phòng ban", required=True, store=True)
    ten_phong_ban = fields.Text("Tên phòng ban")
    chuc_vu_ids = fields.One2many(comodel_name='chuc_vu', inverse_name='phong_ban_id', string="Chức vụ")
    nhan_vien_ids = fields.Many2many(comodel_name='nhan_vien', string="Nhân viên")
