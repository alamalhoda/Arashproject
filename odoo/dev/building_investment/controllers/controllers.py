# -*- coding: utf-8 -*-
# from odoo import http


# class RsLearnModule(http.Controller):
#     @http.route('/rs_learn_module/rs_learn_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rs_learn_module/rs_learn_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rs_learn_module.listing', {
#             'root': '/rs_learn_module/rs_learn_module',
#             'objects': http.request.env['rs_learn_module.rs_learn_module'].search([]),
#         })

#     @http.route('/rs_learn_module/rs_learn_module/objects/<model("rs_learn_module.rs_learn_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rs_learn_module.object', {
#             'object': obj
#         })
