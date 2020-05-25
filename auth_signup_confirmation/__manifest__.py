{
    'name': 'Email confirmation on sign up',
    'version': '13.0.1.0.0',
    'category': 'Website',
    'summary': 'Email Confirmation after signup',
    'description': """

    """,
    'sequence': 1,
    'author': 'Toolkit',
    'website': 'http://toolkt.com',
    'depends': ['auth_signup','website'],
    'data': [
        'data/config.xml', 
        'views/thankyou.xml', 
        'data/email.xml'
    ],
    'images': [
        # 'static/description/auth_signup_banner.png',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
    'post_init_hook': 'init_auth',
}