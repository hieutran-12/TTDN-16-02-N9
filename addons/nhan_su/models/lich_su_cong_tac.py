from odoo import models, fields, api

class LichSuCongTac(models.Model):
    _name = 'lich_su_cong_tac'
    _description = 'Bảng chứa thông tin nhân viên'

    nhan_vien_id = fields.Many2one(comodel_name="nhan_vien", string="Nhân viên", required=True)
    phong_ban_id = fields.Many2one(comodel_name="phong_ban", string="Phòng Ban", required=True)
    chuc_vu_id = fields.Many2one(comodel_name="chuc_vu", string="Chức Vụ", required=True)
    loai_chuc_vu = fields.Selection(
        [
            ("Chính", "Chính"),
            ("Kiêm nhiệm", "Kiêm nhiệm"),
        ],
        string="Loại chức vụ",
        default="Chính"
    )
    ngay_bat_dau = fields.Date("Ngày bắt đầu")
    ngay_ket_thuc = fields.Date("Ngày kết thúc")
    mo_ta = fields.Text("Mô tả")