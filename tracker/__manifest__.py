# -*- coding: utf-8 -*-
{
    'name': "ITR Tracker",

    'summary': """
        Income Tax Return Monitoring System""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Rann Aureada",
    'website': "https://www.amyucpas.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'FS Tracker',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/main_view.xml',
        'views/tracker_process_view.xml',
        'views/groups_view.xml',
        # 'views/menu_view.xml',
        # 'views/process_view.xml',

    ],
    'application': True,
    'license': 'LGPL-3',
}
