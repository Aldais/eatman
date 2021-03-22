# -*- coding: utf-8 -*-
# from odoo import http


# class Eatman(http.Controller):
#     @http.route('/eatman/eatman/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/eatman/eatman/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('eatman.listing', {
#             'root': '/eatman/eatman',
#             'objects': http.request.env['eatman.eatman'].search([]),
#         })

#     @http.route('/eatman/eatman/objects/<model("eatman.eatman"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('eatman.object', {
#             'object': obj
#         })
