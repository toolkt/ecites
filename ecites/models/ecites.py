# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError, AccessError, UserError




class eCitesSource(models.Model):
    _name = 'ecites.source'

    name = fields.Char(string='Description')
    code = fields.Char(string='Code')

class eCitesPurpose(models.Model):
    _name = 'ecites.purpose'

    name = fields.Char(string='Description')
    code = fields.Char(string='Code')


class eCitesSpecies(models.Model):
    _name = 'ecites.species'

    name = fields.Char(string='Full Name', copy=False)
    s_english_name1 = fields.Char(string='English Name 1', copy=False)
    s_english_name2 = fields.Char(string='English Name 2', copy=False)
    s_kingdom = fields.Char(string='Kingdom')
    s_class = fields.Char(string='Class')
    s_current_listing = fields.Char(string='Current Listing')
    s_type = fields.Selection([('Flora','Flora'),('Fauna','Fauna')], 'Type')
    s_category = fields.Selection([('Flora','Flora'),('Fauna','Fauna')], 'Type')
    s_order = fields.Char(string='Order')
    s_family = fields.Char(string='Family')



class ResPartner(models.Model):
    _inherit = "res.partner"

    company = fields.Char('Name of Establishment / Company')
    permit_no = fields.Char(string='Wildlife Farm Permit No. (if applicable)')
    permit_date_issued = fields.Char(string='Date Issued')
    authorized_rep = fields.Char(string='Name of authorized representative')
    authorized_rep_contact_no = fields.Char(string='Contact number')



class eCitesApplication(models.Model):
    _name = 'ecites.application'
    _inherit = ['mail.thread']


    @api.model
    def create(self, vals):
        rec = super(eCitesApplication, self).create(vals)
        rec.name = self.env['ir.sequence'].next_by_code('ecites.application')
        return rec

    name = fields.Char(string='Number', copy=False)

    permit_type = fields.Selection([('export','CITES Export Permit'),('import','CITES Import Permit'),('re-export','CITES Re-export Permit')], required=True, string='Type of permit')
    importer_name = fields.Char(string='Importer', required=True )
    company_name = fields.Char(string='Company')
    company_address = fields.Char(string='Address', required=True)
    purpose = fields.Many2one('ecites.purpose',string='Purpose', required=True)
    shipment_date = fields.Date(string='Shipment Date', required=True)
    transport_type = fields.Char(string='Transport Type')

    line_ids = fields.One2many('ecites.application.line','application_id', "Items")
    state = fields.Selection([('draft','Draft'),('submitted','Submitted'),('approved','Approved'),('cancelled','Cancelled')], 'Status')




class eCitesApplicationLine(models.Model):
    _name = 'ecites.application.line'



    @api.onchange('s_category')
    def onchange_s_category(self):
        return {'domain': {'s_name': [('s_type', '=', self.s_category)]}}


    @api.onchange('s_name')
    def onchange_s_name(self):
        self.s_common_name = self.s_name.s_english_name1

    application_id = fields.Many2one('ecites.application', "Application Id")

    s_category = fields.Selection([('Flora','Flora'),('Fauna','Fauna')], 'Category')
    s_name = fields.Many2one('ecites.species',string='Scientific Name')
    s_common_name = fields.Char(string='Common Name')
    cites_appendix = fields.Char(string='CITES Appendix')

    quantity = fields.Integer(string='Quantity')
    unit = fields.Char(string='Unit')

    source = fields.Many2one('ecites.source','Source')
    name = fields.Text('Description')

    file_ir = fields.Binary("Inspection Report")
    file_ltp = fields.Binary("Local Transport Permit (LTP)")
    file_as = fields.Binary("Addl Support Docs")
