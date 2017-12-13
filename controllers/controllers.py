# -*- coding: utf-8 -*-
from odoo import http

# class HwScaleSale(http.Controller):
#     @http.route('/hw_scale_sale/hw_scale_sale/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hw_scale_sale/hw_scale_sale/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hw_scale_sale.listing', {
#             'root': '/hw_scale_sale/hw_scale_sale',
#             'objects': http.request.env['hw_scale_sale.hw_scale_sale'].search([]),
#         })

#     @http.route('/hw_scale_sale/hw_scale_sale/objects/<model("hw_scale_sale.hw_scale_sale"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hw_scale_sale.object', {
#             'object': obj
#         })