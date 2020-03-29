# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Philippines Address',
    'category': 'Base',
    'summary': 'Philippine Addresses',
    'version': '0.1',
    'description': """
Philippine Addresses
Region
Province
City
Barangay
""",
    'depends': [],
    'data': [
        'data/ir.model.access.csv',
        
        'data/res_region_data.xml',
        'data/res_province_data.xml',
        'data/res_citymun_data.xml',
        # 'data/res_brgy_data.xml',

        'res_address_view.xml',
        'users_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
