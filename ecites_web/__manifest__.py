{
    'name': 'ECites Web',
    'version': '13.0.1.0.0',
    'category': 'Website',
    'summary': 'ECites Website',
    'description': """

    """,
    'sequence': 1,
    'author': 'Toolkit',
    'website': 'http://toolkt.com',
    'depends': ['portal'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'data/sequence.xml',
        'data/ecites_purpose_data.xml',
        'data/ecites_source_data.xml',
        'data/ecites_species_data.xml',

    ],
    'images': [
        # 'static/description/auth_signup_banner.png',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3'
}
