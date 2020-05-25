# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError, AccessError, UserError




class ResPartner(models.Model):
    _inherit = "res.partner"

    company = fields.Char('Establishment/Company')
    permit_no = fields.Char(string='Wildlife Farm Permit No. (if applicable)')
    permit_date_issued = fields.Char(string='Date Issued')
    authorized_rep = fields.Char(string='Name of authorized representative')
    authorized_rep_contact_no = fields.Char(string='Contact number')
    approved_registration = fields.Boolean(string="Approved Registration")
    accept = fields.Boolean('Accept Terms and Conditions')
    registration_status = fields.Selection([('new','New'),('pending','Pending'),('approved','Approved')], default='new')

    brgy = fields.Char(string='Barangay')
    citymun = fields.Char(string='City / Municipality')
    province = fields.Char(string='Province')
    region = fields.Char(string='Region')

    email_2 = fields.Char('Email')
    phone_2 = fields.Char('Phone')
    street_2 = fields.Char('House No.')
    street2_2 = fields.Char('Street / Subd.')
    brgy_2 = fields.Char(string='Barangay')
    citymun_2 = fields.Char(string='City / Municipality')
    province_2 = fields.Char(string='Province')
    region_2 = fields.Char(string='Region')
