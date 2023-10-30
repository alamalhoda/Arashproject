import odoo
from odoo import api, models
from odoo.modules import module

module = module.load_openerp_module('building_investment')
from odoo.addons.building_investment import models

# pool = odoo.registry('db2')
# cr = pool.cursor()
Investment = models.investor.Investment
# ایجاد یک رکورد جدید
inv = Investment()

# چاپ نام مدل Investment
print(Investment)

# چاپ شیء inv
print(inv)

# جستجوی تعداد رکوردها
rec_count = inv.search_count(args=[])
print(rec_count)


# from odoo import models
# from odoo.modules import module
#
# # بارگذاری ماژول
# module = module.load_openerp_module('building_investment')
#
# # ایجاد شیء env
# env = module.registry('db2')['building_investment']
#
# # ایجاد شیء cursor
# cr = env.cr()
#
# # دسترسی به مدل Investment
# Investment = env['building_investment.investor.investment']
#
# # ایجاد یک رکورد جدید
# inv = Investment()
#
# # چاپ نام مدل Investment
# print(Investment._name)
#
# # چاپ شیء inv
# print(inv)
#
# # جستجوی تعداد رکوردها
# rec_count = Investment.search_count([('state', '=', 'active')])
# print(rec_count)