# -*- coding: utf-8 -*-
# from odoo import http


# class TaiChinhKeToan(http.Controller):
#     @http.route('/tai_chinh_ke_toan/tai_chinh_ke_toan', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tai_chinh_ke_toan/tai_chinh_ke_toan/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tai_chinh_ke_toan.listing', {
#             'root': '/tai_chinh_ke_toan/tai_chinh_ke_toan',
#             'objects': http.request.env['tai_chinh_ke_toan.tai_chinh_ke_toan'].search([]),
#         })

#     @http.route('/tai_chinh_ke_toan/tai_chinh_ke_toan/objects/<model("tai_chinh_ke_toan.tai_chinh_ke_toan"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tai_chinh_ke_toan.object', {
#             'object': obj
#         })
