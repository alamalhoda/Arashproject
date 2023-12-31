# -*- coding: utf-8 -*-
{
    'name': "odoo_jalaali",

    'summary': """
        It will show the jalaali date for most of date fields""",

    'description': """
        
    """,

    'author': "Arash Homayounfar",
    'website': "https://karvazendegi.com/odoo",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Service Desk/Service Desk',
    'application': False,
    'version': '15.2.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        ],

    'assets': {
        # 'web._assets_common_scripts': [
        'web.assets_backend': [
            'jalaali-15/static/js/mytime.js',
            'jalaali-15/static/js/moment-jalaali.js',
            'jalaali-15/static/js/daterangepicker_fixed.js',
            'jalaali-15/static/js/tempusdominus_fixed.js',
            'jalaali-15/static/js/fullcalendar_fixed.js',
            ],
        },
    'license': 'LGPL-3',
}
