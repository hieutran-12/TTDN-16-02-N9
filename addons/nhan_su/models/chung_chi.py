from odoo import models, fields, api


class ChungChi(models.Model):
    _name = 'chung_chi'
    _description = 'Bảng chứa thông tin chứng chỉ'
    _order = 'ma_chung_chi'
    _rec_name = "ten_chung_chi"

    ma_chung_chi = fields.Char("Mã định danh", required=True, store=True)
    ten_chung_chi = fields.Text("Chứng chỉ bằng cấp")
    ghi_chu = fields.Text("Ghi chú")
    nhan_vien_id = fields.Many2one(comodel_name='nhan_vien', string="Nhân viên", store=True)
