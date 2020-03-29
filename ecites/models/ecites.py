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
    product_id = fields.Many2one('product.product', "Product")



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


    def action_submit1(self):
        for rec in self:
            rec.write({'state':'submitted'})
            print(rec)


    def action_submit(self):
        """ Called by the 'Fiscal Year Opening' button of the setup bar."""
        # company = self.env.company
        # company.create_op_move_if_non_existant()
        # new_wizard = self.env['my.wizard'].create({'company_id': company.id})
        new_wizard = self.env['ecites.submit.wizard'].create({
                'rec_id':self.id,
                'applicant': self.applicant,
                'company_name': self.company_name,
                'company_address': self.company_address,
                'brgy_id': self.brgy_id.id,
                'citymun_id': self.citymun_id.id,
                'province_id': self.province_id.id,
                'region_id': self.region_id.id,
                'phone': self.phone,
                'email': self.email,
                'permit_no': self.permit_no,
                'permit_date_issued': self.permit_date_issued,
                'authorized_rep': self.authorized_rep,
                'authorized_rep_contact_no': self.authorized_rep_contact_no,
                'digital_signature': self.digital_signature,
            })
        view_id = self.env.ref('ecites.ecites_submit_wizard_form').id

        return {
            'type': 'ir.actions.act_window',
            'name': 'Test Wizard',
            'view_mode': 'form',
            'res_model': 'ecites.submit.wizard',
            'target': 'new',
            'res_id': new_wizard.id,
            'views': [[view_id, 'form']],
        }


    def action_approve(self):
        for rec in self:
            rec.write({'state':'approved'})
            print(rec)


    @api.depends('line_ids')
    def _compute_total(self):
        total = 0.0
        for l in self.line_ids:
            total += l.line_total
        self.total = total


    @api.model
    def create(self, vals):
        rec = super(eCitesApplication, self).create(vals)
        rec.name = self.env['ir.sequence'].next_by_code('ecites.application')
        return rec


    @api.onchange('region_id')
    def onchange_region_idy(self):
        self.province_id = False
        self.citymun_id = False
        self.brgy_id = False
        return {'domain': {'province_id': [('region_id', '=', self.region_id.id)]}}

    @api.onchange('province_id')
    def onchange_province_id(self):
        self.citymun_id = False
        self.brgy_id = False
        return {'domain': {'citymun_id': [('province_id', '=', self.province_id.id)]}}

    @api.onchange('citymun_id')
    def onchange_citymun_id(self):
        self.brgy_id = False
        return {'domain': {'brgy_id': [('citymun_id', '=', self.citymun_id.id)]}}



    name = fields.Char(string='Number', copy=False)

    permit_type = fields.Selection([('export','CITES Export Permit'),('import','CITES Import Permit'),('re-export','CITES Re-export Permit')], required=True, string='Type of permit')
    importer_name = fields.Char(string='Importer', required=True )
    company_name = fields.Char(string='Company')
    company_address = fields.Text(string='Address', required=True)
    purpose = fields.Many2one('ecites.purpose',string='Purpose', required=True)
    shipment_date = fields.Date(string='Shipment Date', required=True)
    transport_type = fields.Char(string='Transport Type')

    line_ids = fields.One2many('ecites.application.line','application_id', "Items")
    state = fields.Selection([('draft','Draft'),('submitted','Submitted'),('approved','Approved'),('cancelled','Cancelled')], default="draft", string='Status')
    total = fields.Float("Total", compute='_compute_total')


    applicant = fields.Char("Applicant Name")

    brgy_id = fields.Many2one('res.brgy', string='Barangay')
    citymun_id = fields.Many2one('res.citymun', string='City / Municipality')
    province_id = fields.Many2one('res.province', string='Province')
    region_id = fields.Many2one('res.region', string='Region')

    complete_address = fields.Text('Complete Address')
    complete_address_disp = fields.Text('Complete Address', related="complete_address")

    phone = fields.Char("Contact Number")
    email = fields.Char("Email Address")

    permit_no = fields.Char(string='Wildlife Farm Permit No. (if applicable)')
    permit_date_issued = fields.Date(string='Date Issued')
    authorized_rep = fields.Char(string='Name of authorized representative')
    authorized_rep_contact_no = fields.Char(string='Contact number')
    digital_signature = fields.Binary(string='Signature')



class eCitesApplicationLine(models.Model):
    _name = 'ecites.application.line'



    @api.onchange('s_category')
    def onchange_s_category(self):
        self.s_name = False
        return {'domain': {'s_name': [('s_type', '=', self.s_category)]}}


    @api.onchange('s_name')
    def onchange_s_name(self):
        self.s_common_name = self.s_name.s_english_name1
        self.price = self.s_name.product_id.list_price

    @api.onchange('quantity')
    def onchange_quantity(self):
        self.line_total = self.quantity*self.price


    application_id = fields.Many2one('ecites.application', "Application Id")

    s_category = fields.Selection([('Flora','Flora'),('Fauna','Fauna')], 'Category')
    s_name = fields.Many2one('ecites.species',string='Scientific Name')
    s_common_name = fields.Char(string='Common Name')
    cites_appendix = fields.Char(string='CITES Appendix')

    quantity = fields.Integer(string='Quantity')
    unit = fields.Char(string='Unit')
    price = fields.Float('Price')
    line_total = fields.Float('Total')

    source = fields.Many2one('ecites.source','Source')
    name = fields.Text('Description')

    file_ir = fields.Binary("Inspection Report")
    file_ltp = fields.Binary("Local Transport Permit (LTP)")
    file_as = fields.Binary("Addl Support Docs")



class eCitesSubmitWizard(models.TransientModel):
    _name = 'ecites.submit.wizard'
    _inherit = ['multi.step.wizard.mixin']


    @api.model
    def _selection_state(self):
        return [
            ('start', 'Applicant Details'),
            ('permit', 'Permit Details'),
            ('sign', 'Sign'),
            ('final', 'Submitted'),
        ]

    @api.onchange('region_id')
    def onchange_region_idy(self):
        self.province_id = False
        self.citymun_id = False
        self.brgy_id = False
        return {'domain': {'province_id': [('region_id', '=', self.region_id.id)]}}

    @api.onchange('province_id')
    def onchange_province_id(self):
        self.citymun_id = False
        self.brgy_id = False
        return {'domain': {'citymun_id': [('province_id', '=', self.province_id.id)]}}

    @api.onchange('citymun_id')
    def onchange_citymun_id(self):
        self.brgy_id = False
        return {'domain': {'brgy_id': [('citymun_id', '=', self.citymun_id.id)]}}



    rec_id = fields.Many2one(
        comodel_name='ecites.application',
        name="Application",
        required=True,
        ondelete='cascade',
    )


    applicant = fields.Char("Applicant Name")
    company_name = fields.Char("Company")
    company_address = fields.Text("Address")

    brgy_id = fields.Many2one('res.brgy', string='Barangay')
    citymun_id = fields.Many2one('res.citymun', string='City / Municipality')
    province_id = fields.Many2one('res.province', string='Province')
    region_id = fields.Many2one('res.region', string='Region')

    complete_address = fields.Text('Complete Address')
    complete_address_disp = fields.Text('Complete Address', related="complete_address")
    phone = fields.Char("Contact Number")
    email = fields.Char("Email Address")

    permit_no = fields.Char(string='Wildlife Farm Permit No. (if applicable)')
    permit_date_issued = fields.Date(string='Date Issued')
    authorized_rep = fields.Char(string='Name of authorized representative')
    authorized_rep_contact_no = fields.Char(string='Contact number')
    digital_signature = fields.Binary(string='Signature')


    def state_exit_start(self):
        self.state = 'permit'


    def state_prev_permit(self):
        self.state = 'start'
    def state_exit_permit(self):
        self.state = 'sign'

    def state_prev_sign(self):
        self.state = 'permit'
    def state_exit_sign(self):
        self.rec_id.write({
                'applicant': self.applicant,
                'company_name': self.company_name,
                'company_address': self.company_address,
                'brgy_id': self.brgy_id.id,
                'citymun_id': self.citymun_id.id,
                'province_id': self.province_id.id,
                'region_id': self.region_id.id,
                'phone': self.phone,
                'email': self.email,
                'permit_no': self.permit_no,
                'permit_date_issued': self.permit_date_issued,
                'authorized_rep': self.authorized_rep,
                'authorized_rep_contact_no': self.authorized_rep_contact_no,
                'digital_signature': self.digital_signature,
                'state':'submitted',
            })


        self.state = 'final'


    def state_exit_final(self):
        return True


class MyWizard(models.TransientModel):
    _name = 'my.wizard'
    _inherit = ['multi.step.wizard.mixin']

    project_id = fields.Many2one(
        comodel_name='ecites.application',
        name="Application",
        # required=True,
        ondelete='cascade',
        # default=lambda self: self._default_project_id(),
    )
    name = fields.Char()
    field1 = fields.Char()
    field2 = fields.Char()
    field3 = fields.Char()

    @api.model
    def _selection_state(self):
        return [
            ('start', 'Start'),
            ('configure', 'Configure'),
            ('custom', 'Customize'),
            ('final', 'Final'),
        ]

    @api.model
    def _default_project_id(self):
        return self.env.context.get('active_id')


    def state_prev_start(self):
        return {'type': 'ir.actions.act_window_close'}

    def state_exit_start(self):
        self.state = 'configure'


    def state_prev_configure(self):
        self.state = 'start'
    def state_exit_configure(self):
        self.state = 'custom'



    def state_prev_custom(self):
        self.state = 'configure'   
    def state_exit_custom(self):
        self.state = 'final'    
