{
    'name': 'PartnershipOS Project',
    'version': '17.0.1.0.0',
    'category': 'PartnershipOS',
    'summary': 'Links Partnership opportunities to project execution and auto-creates projects',
    'author': 'PartnershipOS',
    'depends': ['partnership_os_crm', 'project', 'base_automation'],
    'data': [
        'data/automation_rules.xml',
        'views/project_views.xml',
        'views/crm_lead_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
