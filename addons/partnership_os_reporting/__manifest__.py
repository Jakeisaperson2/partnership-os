{
    'name': 'PartnershipOS Reporting',
    'version': '17.0.1.0.0',
    'category': 'PartnershipOS',
    'summary': 'BD-focused dashboards: revenue by partner, pipeline value, quarterly metrics',
    'author': 'PartnershipOS',
    'depends': ['partnership_os_project', 'account', 'spreadsheet_dashboard'],
    'data': [
        'views/account_dashboard_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
