from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ChiTietButToan(models.Model):
    _name = 'chi_tiet_but_toan'
    _description = 'Chi tiết bút toán'
    _order = 'but_toan_id, id'

    but_toan_id = fields.Many2one('but_toan_ke_toan', string='Bút toán', required=True, ondelete='cascade')
    tai_khoan_id = fields.Many2one('tai_khoan_ke_toan', string='Tài khoản', required=True)
    dien_giai = fields.Text('Diễn giải')
    tien_no = fields.Monetary('Tiền Nợ', default=0)
    tien_co = fields.Monetary('Tiền Có', default=0)
    doi_tac_id = fields.Many2one('res.partner', string='Đối tác')
    currency_id = fields.Many2one('res.currency', related='but_toan_id.currency_id', store=True, readonly=True)

    @api.constrains('tien_no', 'tien_co')
    def _check_no_co(self):
        for rec in self:
            if rec.tien_no > 0 and rec.tien_co > 0:
                raise ValidationError(_('Chỉ được nhập Nợ hoặc Có, không được nhập cả hai!'))
            if rec.tien_no == 0 and rec.tien_co == 0:
                raise ValidationError(_('Phải nhập Nợ hoặc Có!'))
