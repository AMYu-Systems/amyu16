# -*- coding: utf-8 -*-
{
    'name': "Billing And Collection System",
    'summary': """
        Billing and Collection Details Information""",
    'description': """
        Long description of module's purpose
    """,
    'author': "Rann Aureada",
    'website': "https://www.amyucpas.com",
    'category': 'Custom',
    'version': '0.1',
    'depends': ['base', 'muk_web_theme'],

    # always loaded
    'data': ['security/ir.model.access.csv',
             'views/base_billing_view.xml',
             'views/billing_summary_view.xml',
             'views/audit_billing_view.xml',
             'views/trc_billing_view.xml',
             'views/books_billing_view.xml',
             'views/business_permit_billing_view.xml',
             'views/gis_billing_view.xml',
             'views/loa_billing_view.xml',
             'views/special_engagement_view.xml',
             'views/services_type_view.xml',
             'views/bcs_billing_view.xml',
             'views/bcs_collection_view.xml',
             'views/bcs_update_view.xml',
             'views/state_billing_view.xml',
             'views/bcs_group_view.xml',
             'views/bcs_menu_view.xml',
             ],
    'application': True,
    'license': 'LGPL-3',
}
