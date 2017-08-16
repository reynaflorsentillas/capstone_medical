# -*- coding: utf-8 -*-
from odoo import http

# class MedicalBase(http.Controller):
#     @http.route('/medical_base/medical_base/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/medical_base/medical_base/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('medical_base.listing', {
#             'root': '/medical_base/medical_base',
#             'objects': http.request.env['medical_base.medical_base'].search([]),
#         })

#     @http.route('/medical_base/medical_base/objects/<model("medical_base.medical_base"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('medical_base.object', {
#             'object': obj
#         })