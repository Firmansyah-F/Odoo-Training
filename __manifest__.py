# -*- coding: utf-8 -*-
{
    'name': "xti_training",

    'summary': """
        XTI Training 2022""",

    'description': """
        XTI Training 2022 - 19 = Desember
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'account', 'portal', 'utm'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/service_security.xml',
        'reports/service_report.xml',
        'sequence/sequence.xml',
        'views/views.xml',
        'views/car.xml',
        'views/templates.xml',
        'wizards/service_wizard.xml',
        'data/scheduler.xml',
        'data/server_action.xml',
        'data/system_parameter.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
