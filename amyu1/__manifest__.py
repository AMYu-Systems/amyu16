# -*- coding: utf-8 -*-
{
    'name': "A.M.Yu & ASSOCIATES",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Rann Aureada",
    'website': "https://www.amyucpas.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'muk_web_theme'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/associates_profile_view.xml',
        'views/client_profile_view.xml',
        'views/corporate_officer_view.xml',
        'views/class_of_shares_view.xml',
        'views/escalation_contact.xml',
        'views/client_records_views.xml',

    ],
    'application': True,
}
