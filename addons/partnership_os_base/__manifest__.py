{
    'name': 'PartnershipOS Base',
    'version': '17.0.1.0.0',
    'category': 'PartnershipOS',
    'summary': 'Foundation: navigation cleanup and brand identity for PartnershipOS',
    'author': 'PartnershipOS',
    'depends': ['web', 'base', 'mail'],
    'data': [],
    'assets': {
        'web._assets_primary_variables': [
            ('prepend', 'partnership_os_base/static/src/scss/branding.scss'),
        ],
    },
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
