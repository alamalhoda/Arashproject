import odoo
from odoo.addons.base.models.ir_module import Module
from odoo.modules import module

from odoo.addons.base.models.res_users import Users
from odoo.addons.building_investment import models
from odoo.addons.building_investment.models.investor import Investment

print('------------')
# module = module.load_openerp_module('building_investment')
registry = odoo.registry()
cr = registry.cursor()
env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
users: Users = env['res.users']
modules: Module = env['ir.module.module']
# modules.sudo().update_list()
building_investment = modules.search([('name', '=', 'building_investment')])
print(f"{building_investment.name}")

inv: Investment = env['building_investment.investment']
inv_count = inv.search([('amount', '>', '20000')])
# for i in inv_count:
#     i._compute_date_shamsi_year_month()

    # print(f"{i.date_shamsi_year_month}")

model = env['building_investment.investment']
env.add_to_compute(model._fields['date_shamsi_year_month'], model.search([]))
model.recompute()
env.cr.commit()
cr.close()
# print(len(inv_count))
