from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class TaiKhoanKeToan(models.Model):
    _name = 'tai_khoan_ke_toan'
    _description = 'Tài khoản kế toán'
    _rec_name = 'ma_tai_khoan'
    _order = 'ma_tai_khoan'

    ma_tai_khoan = fields.Char('Mã tài khoản', required=True, index=True)
    ten_tai_khoan = fields.Char('Tên tài khoản', required=True)
    loai_tai_khoan = fields.Selection([
        ('tai_san', 'Tài sản'),
        ('no_phai_tra', 'Nợ phải trả'),
        ('von_chu_so_huu', 'Vốn chủ sở hữu'),
        ('doanh_thu', 'Doanh thu'),
        ('chi_phi', 'Chi phí'),
    ], string='Loại tài khoản', required=True)
    tai_khoan_cha_id = fields.Many2one('tai_khoan_ke_toan', string='Tài khoản cha')
    la_tai_khoan_tong_hop = fields.Boolean('Tài khoản tổng hợp', default=False)
    active = fields.Boolean('Kích hoạt', default=True)
    currency_id = fields.Many2one('res.currency', string='Tiền tệ', default=lambda self: self.env.company.currency_id)
    du_no = fields.Monetary('Dư Nợ', compute='_compute_du_no_co', store=True, currency_field='currency_id')
    du_co = fields.Monetary('Dư Có', compute='_compute_du_no_co', store=True, currency_field='currency_id')
    chi_tiet_ids = fields.One2many('chi_tiet_but_toan', 'tai_khoan_id', string='Chi tiết')

    _sql_constraints = [
        ('ma_tai_khoan_unique', 'unique(ma_tai_khoan)', 'Mã tài khoản phải là duy nhất!'),
    ]

    def name_get(self):
        result = []
        for rec in self:
            name = f"{rec.ma_tai_khoan} - {rec.ten_tai_khoan}"
            result.append((rec.id, name))
        return result

    @api.depends('chi_tiet_ids.tien_no', 'chi_tiet_ids.tien_co')
    def _compute_du_no_co(self):
        for rec in self:
            tong_no = sum(line.tien_no for line in rec.chi_tiet_ids if line.but_toan_id.state == 'da_ghi_so')
            tong_co = sum(line.tien_co for line in rec.chi_tiet_ids if line.but_toan_id.state == 'da_ghi_so')
            rec.du_no = max(0, tong_no - tong_co)
            rec.du_co = max(0, tong_co - tong_no)
