# -*- coding: utf-8 -*-
{
    'name': "A.M.Yu & ASSOCIATES",

    'summary': """
        Client Profile and Monitoring System""",

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
    'depends': ['base', 'mail', 'resource'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/cpms_groups.xml',
        'views/cpms_state_view.xml',
        'views/associates_profile_view.xml',
        'views/client_profile_view.xml',
        'views/cpms_client_list_view.xml',
        'views/supervisor_view.xml',
        'views/manager_view.xml',
        'views/corporate_officer_view.xml',
        'views/class_of_shares_view.xml',
        'views/escalation_contact.xml',
        'views/client_records_views.xml',
        'views/cmps_menu_view.xml',
    ],
    'application': True,
    'license': 'LGPL-3',

}
