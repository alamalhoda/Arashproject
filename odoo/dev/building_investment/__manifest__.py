# -*- coding: utf-8 -*-
{
    'name': "building investment",

    'summary': """
for building investment. 3
""",

    'description': """
for building investment.    """,

    'author': "royaSoftGroup",
    'website': "http://www.royaSoftGroup.ir",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
       'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
       'views/investment_views.xml',
    ],
    'sequence': 1,
    'application': True,
    'license': 'LGPL-3',
    'installable': True,
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
