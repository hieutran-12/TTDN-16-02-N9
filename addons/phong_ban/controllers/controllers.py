# -*- coding: utf-8 -*-
# from odoo import http


# class NhanSu(http.Controller):
#     @http.route('/phong_ban/phong_ban', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/phong_ban/phong_ban/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('phong_ban.listing', {
#             'root': '/phong_ban/phong_ban',
#             'objects': http.request.env['phong_ban.phong_ban'].search([]),
#         })

#     @http.route('/phong_ban/phong_ban/objects/<model("phong_ban.phong_ban"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('phong_ban.object', {
#             'object': obj
#         })
