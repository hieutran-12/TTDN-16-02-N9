import datetime
import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ho_ten'
    _order = 'ma_dinh_danh'
    _sql_constraints = [
        ('ma_dinh_danh_unique', 'unique(ma_dinh_danh)', 'Mã định danh phải là duy nhất!')
    ]

    ma_dinh_danh = fields.Char("Mã định danh", required=True)
    ho_ten = fields.Char("Họ và tên", required=True)
    ngay_sinh = fields.Date("Ngày sinh")
    que_quan = fields.Char("Quê quán")
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại")
    phong_ban_ids = fields.Many2many(comodel_name='phong_ban', string="Phòng ban")
    lich_su_cong_tac_ids = fields.One2many(comodel_name='lich_su_cong_tac', inverse_name="nhan_vien_id",
                                           string="Lịch sử công tác")
    chung_chi_ids = fields.One2many(comodel_name='chung_chi', inverse_name="nhan_vien_id",
                                    string="Chứng chỉ")
    tuoi = fields.Integer(string="Tuổi", compute='_compute_tuoi', store=True)
    thang_sinh = fields.Integer(string="Tháng sinh", compute='_compute_thang_sinh', store=True)

    @api.depends("ngay_sinh")
    def _compute_tuoi(self):
        for record in self:
            if record.ngay_sinh:
                record.tuoi = datetime.date.today().year - record.ngay_sinh.year

    @api.onchange("ngay_sinh")
    def _compute_thang_sinh(self):
        for record in self:
            if record.ngay_sinh:
                record.thang_sinh = record.ngay_sinh.month

    @api.constrains('tuoi')
    def _check_tuoi(self):
        for record in self:
            if record.tuoi < 18:
                raise ValidationError("Tuổi bé hơn 18")

    @api.constrains('email')
    def _check_email(self):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        for record in self:
            if record.email and not re.match(email_regex, record.email):
                raise ValidationError("Email không hợp lệ!")

    @api.constrains('so_dien_thoai')
    def _check_so_dien_thoai(self):
        phone_regex = r'^\d{10,11}$'
        for record in self:
            if record.so_dien_thoai and not re.match(phone_regex, record.so_dien_thoai):
                raise ValidationError("Số điện thoại không hợp lệ! Phải có 10 hoặc 11 chữ số.")
