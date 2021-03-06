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
    'depends': ['base','base_address_ph','website','auth_signup','multi_step_wizard','web_digital_sign','portal','tk_pentaho_reports_odoo_v13'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'data/sequence.xml',
        'data/ecites_purpose_data.xml',
        'data/ecites_source_data.xml',
        'data/ecites_species_data.xml',

        'views/website/assets.xml',
        'views/website/portal_templates.xml',
        'views/website/website_permit.xml',
        'views/website/website_permit_apply.xml',
        'views/website/website_permit_status.xml',
        'views/website/website_my_permit_application.xml',
        'views/website/website_complete_registration.xml',



        'views/ecites_view.xml',
        'views/master_data_view.xml',
        'views/res_partner_view.xml',
        # 'views/auth_signup_extended_views.xml',
        'views/wizard_test.xml',
        'views/portal_template.xml',

        'reports/report.xml',






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
