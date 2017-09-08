# -*- coding: utf-8 -*-
from odoo import http

# class MedicalWebsite(http.Controller):
#     @http.route('/medical_website/medical_website/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/medical_website/medical_website/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('medical_website.listing', {
#             'root': '/medical_website/medical_website',
#             'objects': http.request.env['medical_website.medical_website'].search([]),
#         })

#     @http.route('/medical_website/medical_website/objects/<model("medical_website.medical_website"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('medical_website.object', {
#             'object': obj
#         })