# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from odoo.osv import expression
from odoo import api, SUPERUSER_ID

from werkzeug.urls import url_encode
import werkzeug
import binascii
import json

def Merge(dict1, dict2): 
    res = {**dict1, **dict2} 
    return res 

class CustomerPortal(CustomerPortal):
    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id

        EcitesApplication = request.env['ecites.application']
        ecites_application_count = EcitesApplication.search_count([
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
            ('state', 'in', ['draft','submit', 'cancel'])
        ])


        values.update({
            'ecites_application_count': ecites_application_count
        })
        return values

class PermitApplicationProcess(http.Controller):

    @http.route(['/permit/apply'], methods=['GET'], type='http', auth="user", website=True)
    def permit_apply(self, **kw):
        params = werkzeug.url_encode(kw)
        partner = request.env.user.partner_id
        url = '/permit/apply'


        ctx = {'partner' : partner }

        if partner.registration_status == 'new':
            return request.render("ecites.complete_registration",ctx)

        if partner.registration_status == 'pending':
            return request.redirect('/pending-approval')

        
        if params:
            print ("Has Params")
            #Check Application Type
            application_type = kw.get('application_type', '')
            permit_type = kw.get('permit_type', '')
            if application_type and (not permit_type):                
                link = {
                    'export': url+'?'+url_encode(Merge(kw,{'permit_type':'export'})),
                    're-export': url+'?'+url_encode(Merge(kw,{'permit_type':'re-export'})),
                    'import': url+'?'+url_encode(Merge(kw,{'permit_type':'import'})),

                }
                return request.render("ecites.permit_apply",{'link':link, 'page':'permit_type'})

            if not (not application_type or not permit_type):
                url = '/permit/application/form?' + url_encode(kw)
                return request.redirect(url)

            

            return request.redirect('/permit/apply')


        print ("No Params")
        link = {
            'regular': url+'?'+ url_encode({'application_type':'regular'}),
            'walk-in': url+'?'+ url_encode({'application_type':'walk-in'}),
        }
        print (link)
        return request.render("ecites.permit_apply", {'link':link, 'page':'apply'})


    @http.route(['/my/ecites/account'], type='http', auth="user", website=True)
    def permit_complete_registration(self, **post):
        partner = request.env.user.partner_id
        return request.render("ecites.complete_registration",{'partner' : partner })



    @http.route(['/permit/application/form'],methods=['GET', 'POST'], type='http', auth="user", csrf=False, website=True)
    def permit_application_form(self, **post):

        data = post
        partner = request.env.user.partner_id
        if not 'name' in data:
            data['name'] =  partner['name']
        if not 'company' in data:
            data['company'] =  partner['company']
        if not 'street' in data:
            data['street'] =  partner['street']

        fdata = data.pop('fdata')
        print(data)
        
        return request.render("ecites.permit_apply_form",data)




    @http.route(['/my/permit_applications'], type='http', auth="user", website=True)
    def permit_apply_import(self, **post):
        partner = request.env.user.partner_id
        return request.render("ecites.my_permit_applications")


    @http.route(['/application/status/<string:permit_no>'], type='http', auth="user", website=True)
    def permit_apply_import(self, **kw):
        partner = request.env.user.partner_id
        application_no = request.env['ecites.application'].with_user(SUPERUSER_ID).search([('name', '=', kw['permit_no'])],limit=1)[0]
        data = { 'application' : application_no}

        return request.render("ecites.permit_status", data)

