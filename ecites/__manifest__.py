{
    'name': 'ECites',
    'version': '13.0.1.0.0',
    'category': 'Website',
    'summary': 'ECites Website',
    'description': """

    """,
    'sequence': 1,
    'author': 'Toolkit',
    'website': 'http://toolkt.com',
    'depends': ['auth_signup'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',

        'views/ecites_view.xml',
        'views/master_data_view.xml',
        'views/res_partner_view.xml',
        'views/auth_signup_extended_views.xml',
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
