{
    'name': 'PartnershipOS CRM',
    'version': '17.0.1.0.0',
    'category': 'PartnershipOS',
    'summary': 'Transforms CRM into a Partnership Management module for AMCs',
    'author': 'PartnershipOS',
    'depends': ['partnership_os_base', 'crm', 'sales_team'],
    'data': [
        'data/partnership_stages.xml',
        'data/menu_renames.xml',
        'views/crm_lead_views.xml',
        'views/crm_team_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
