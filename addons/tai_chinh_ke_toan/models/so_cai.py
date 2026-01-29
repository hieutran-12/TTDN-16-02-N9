from odoo import models, fields, api

class SoCai(models.Model):
    _name = 'so_cai'
    _description = 'Sổ cái kế toán tổng hợp'
    _auto = False

    but_toan_id = fields.Many2one('but_toan_ke_toan', string='Bút toán')
    ngay_but_toan = fields.Date('Ngày bút toán')
    tai_khoan_id = fields.Many2one('tai_khoan_ke_toan', string='Tài khoản')
    dien_giai = fields.Text('Diễn giải')
    tien_no = fields.Monetary('Tiền Nợ')
    tien_co = fields.Monetary('Tiền Có')
    doi_tac_id = fields.Many2one('res.partner', string='Đối tác')
    currency_id = fields.Many2one('res.currency', string='Tiền tệ')

    def init(self):
        self.env.cr.execute('''
            CREATE OR REPLACE VIEW so_cai AS (
                SELECT
                    row_number() OVER() AS id,
                    ctb.id AS but_toan_id,
                    bt.ngay_but_toan,
                    ctb.tai_khoan_id,
                    ctb.dien_giai,
                    ctb.tien_no,
                    ctb.tien_co,
                    ctb.doi_tac_id,
                    ctb.currency_id
                FROM chi_tiet_but_toan ctb
                JOIN but_toan_ke_toan bt ON ctb.but_toan_id = bt.id
                WHERE bt.state = 'da_ghi_so'
            )
        ''')
