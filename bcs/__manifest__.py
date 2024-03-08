{
    'name': 'Billing and Collection System',
    'author': 'Rann Aureada & Angelo Algarne',
    'category': 'Application',
    'summary': 'AMYU Systems - Billing and Collection System',
    'version': '1.0',
    'description': """
        AMYu Systems - Billing and Collection System. 

        Processes the Billing and Collection of Finance and Audit Department, 
        wherein the prequisites are the client profiles fetched from CPMS, 
        and the clients' Billing Summary.

        As of version 1, the expected generated outputs are the 
        (1) Collection Reports and (2) SOA & Billing Statements. 
    """,
    'depends': ['base', 'hrad'],
    'data': [
        'security/ir.model.access.csv',
        'views/bcs_client_billing_info_views.xml',
        'views/bcs_bank_views.xml',
        'views/bcs_menu_views.xml',
    ],
    'auto_install': True,
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}