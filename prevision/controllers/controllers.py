# -*- coding: utf-8 -*-
# from odoo import http


# class Prevision(http.Controller):
#     @http.route('/prevision/prevision/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/prevision/prevision/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('prevision.listing', {
#             'root': '/prevision/prevision',
#             'objects': http.request.env['prevision.prevision'].search([]),
#         })

#     @http.route('/prevision/prevision/objects/<model("prevision.prevision"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('prevision.object', {
#             'object': obj
#         })
