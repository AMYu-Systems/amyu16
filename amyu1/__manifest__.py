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
    'depends': ['base', 'mail', 'resource', ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/cpms_associate_profile_view.xml',
        'views/client_profile_view.xml',
        'security/cpms_groups.xml',
        'views/cpms_state_view.xml',
        'views/cpms_client_list_view.xml',
        'views/cpms_report_view.xml',
        'views/cpms_team_view.xml',
        'views/supervisor_view.xml',
        'views/manager_view.xml',
        'views/cpms_capital_sole_proprietor_view.xml',
        'views/cpms_capitalization_view.xml',
        'views/cpms_capital_general_partnership_view.xml',
        'views/cpms_capital_professional_partnership_view.xml',
        'views/cpms_capital_domestic_nsnp_view.xml',
        'views/cpms_capital_foreign_corp_view.xml',
        'views/cpms_capital_foreign_nsnp_view.xml',
        'views/cpms_capital_roqh_foreign_view.xml',
        'views/cpms_capital_representative_office_view.xml',
        'views/cpms_sole_proprietor_view.xml',
        'views/cpms_gen_partnership_view.xml',
        'views/cpms_gen_pro_partnership_view.xml',
        'views/cpms_domestic_stock_view.xml',
        'views/cpms_domestic_nsnp_corp_view.xml',
        'views/cpms_foriegn_corp_view.xml',
        'views/cpms_foreign_nsnp_corp_view.xml',
        'views/cpms_roqh_foriegn_corp_view.xml',
        'views/cpms_representative_office_view.xml',
        'views/escalation_contact.xml',
        'views/cmps_menu_view.xml',
        'report/cpms_preview_reports.xml',
        'views/cpms_supervisor_view.xml',

    ],
    'application': True,
    'license': 'LGPL-3',
}
