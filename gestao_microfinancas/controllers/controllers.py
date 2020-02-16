# -*- coding: utf-8 -*-
from odoo import http

# class Microfinancas(http.Controller):
#     @http.route('/gestao_microfinancas/gestao_microfinancas/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestao_microfinancas/gestao_microfinancas/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestao_microfinancas.listing', {
#             'root': '/gestao_microfinancas/gestao_microfinancas',
#             'objects': http.request.env['gestao_microfinancas.gestao_microfinancas'].search([]),
#         })

#     @http.route('/gestao_microfinancas/gestao_microfinancas/objects/<model("gestao_microfinancas.gestao_microfinancas"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestao_microfinancas.object', {
#             'object': obj
#         })