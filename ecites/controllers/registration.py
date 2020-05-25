# -*- coding: utf-8 -*-

import base64

from odoo.http import content_disposition, Controller, request, route
import odoo.addons.portal.controllers.portal as PortalController
from odoo.addons.website.controllers.main import Website
from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo.osv import expression

from odoo import http, tools
import werkzeug


from odoo import http
from odoo.http import request

class RegistrationFlow(http.Controller):
    @http.route(['/registration/submit'], type='http', auth="user", csrf=False, website=True)
    def registration_submit(self, **post):

        print(post)
        
        data = {
            'company': post.get('company'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'street': post.get('street'),
            'street2': post.get('street2'),
            'region': post.get('region'),
            'province': post.get('province'),
            'citymun': post.get('citymun'),
            'region': post.get('region'),
            'brgy': post.get('brgy'),

            'email_2': post.get('email_2'),
            'phone_2': post.get('phone_2'),
            'street_2': post.get('street_2'),
            'street2_2': post.get('street2_2'),
            'region_2': post.get('region_2'),
            'province_2': post.get('province_2'),
            'citymun_2': post.get('citymun_2'),
            'region_2': post.get('region_2'),
            'brgy_2': post.get('brgy_2'),

            'permit_no': post.get('permit_no'),
            'permit_date_issued': post.get('permit_date_issued'),
            'authorized_rep': post.get('authorized_rep'),
            'authorized_rep_contact_no': post.get('authorized_rep_contact_no'),

            'accept': post.get('accept'),

            'registration_status': 'pending'


        }


        request.env.user.partner_id.sudo().write(data)
        return request.redirect('/thank-you-for-registering')


