# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError, AccessError, UserError

import qrcode
import base64
from io import BytesIO


def generate_qr_code(url):
    qr = qrcode.QRCode(
             version=1,
             error_correction=qrcode.constants.ERROR_CORRECT_L,
             box_size=20,
             border=4,
             )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    temp = BytesIO()
    img.save(temp, format="PNG")
    qr_img = base64.b64encode(temp.getvalue())
    return qr_img




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




class eCitesApplication(models.Model):
    _name = 'ecites.application'
    _inherit = ['mail.thread']


    def action_submit(self):
        for rec in self:
            print(rec)

            for application in self.filtered(lambda application: rec.partner_id not in rec.message_partner_ids):
                application.message_subscribe([rec.partner_id.id])

            #Generate Unique Permit Number
            if not rec.name:
                suffix = ''
                if rec.permit_type == 'export':
                    suffix = 'CE'
                if rec.permit_type == 'import':
                    suffix = 'CI'
                if rec.permit_type == 're-export':
                    suffix = 'CR'

                rec.name = "%s%s" % (self.env['ir.sequence'].next_by_code('ecites.application'),suffix)

                #Generate QR Code
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                base_url += '/application/status/%s' % rec.name
                rec.qr_image = generate_qr_code(base_url)

            if rec.state == 'draft':
                rec.write({'state':'submitted'})







    def action_submit_region(self):
        for rec in self:
            rec.write({'state':'region'})


    def action_submit_evaluator(self):
        for rec in self:
            rec.write({'state':'evaluator'})

    def action_submit_payment(self):
        for rec in self:
            rec.write({'state':'payment'})

    def action_submit_wrchief(self):
        for rec in self:
            rec.write({'state':'wrchief'})

    def action_submit_approved(self):
        for rec in self:
            rec.write({'state':'approved'})

    def action_cancel(self):
        for rec in self:
            rec.write({'state':'cancelled'})
            print(rec)


    def action_submit0(self):
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





    @api.depends('line_ids')
    def _compute_total(self):
        total = 0.0
        for l in self.line_ids:
            total += l.line_total
        self.total = total


    # @api.model
    # def create(self, vals):
    #     rec = super(eCitesApplication, self).create(vals)
    #     rec.name = self.env['ir.sequence'].next_by_code('ecites.application')

    #     return rec


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



    name = fields.Char(string='Number', copy=False, tracking=True)

    applicant_type = fields.Selection([('regular','Regular'),('walkin','Walkin')], required=True, string='Applicant Type', tracking=True)
    permit_type = fields.Selection([('export','CITES Export Permit'),('import','CITES Import Permit'),('re-export','CITES Re-export Permit')], required=True, string='Type of permit', tracking=True)
    importer_name = fields.Char(string='Importer', required=True , tracking=True)
    partner_id = fields.Many2one('res.partner', string="Importer User", default=lambda self: self.env.user.partner_id.id, tracking=True)
    company_name = fields.Char(string='Company', tracking=True)
    company_address = fields.Text(string='Address', required=True, tracking=True)
    purpose = fields.Many2one('ecites.purpose',string='Purpose', required=True, tracking=True)
    shipment_date = fields.Date(string='Shipment Date', required=True, tracking=True)
    transport_type = fields.Selection([('air','Air Cargo'),('sea','Sea Cargo'),('post','Postal')], required=True, string='Transport', tracking=True)

    line_ids = fields.One2many('ecites.application.line','application_id', "Items", tracking=True)
    state = fields.Selection([
        ('draft','Draft'),
        ('submitted','Submitted'),
        ('region','Endorsed by Region'),
        ('evaluator','Endorsed by Evaluator'),
        ('payment','Order of Payment'),
        ('wrchief','Endorsed by WR Chief'),
        ('approved','Approved'),
        ('cancelled','Cancelled')
        ], default="draft", string='Status', tracking=True)
    total = fields.Float("Total", compute='_compute_total', tracking=True)


    applicant = fields.Char("Applicant Name", tracking=True)

    brgy_id = fields.Many2one('res.brgy', string='Barangay', tracking=True)
    citymun_id = fields.Many2one('res.citymun', string='City / Municipality', tracking=True)
    province_id = fields.Many2one('res.province', string='Province', tracking=True)
    region_id = fields.Many2one('res.region', string='Region', tracking=True)

    complete_address = fields.Text('Complete Address', tracking=True)
    complete_address_disp = fields.Text('Complete Address', related="complete_address", tracking=True)

    phone = fields.Char("Contact Number", tracking=True)
    email = fields.Char("Email Address", tracking=True)


    authorized_rep = fields.Char(string='Name of authorized representative', tracking=True)
    authorized_rep_contact_no = fields.Char(string='Contact number', tracking=True)
    digital_signature = fields.Binary(string='Signature', tracking=True)

    permit_no = fields.Char(string='Wildlife Farm Permit No. (if applicable)', tracking=True)
    permit_date_issued = fields.Date(string='Date Issued', tracking=True)    
    permit_validity = fields.Date(string='Permit Validity')
    country_exportation = fields.Many2one('res.country',"Country of (re)Exportation")
    country_destination = fields.Many2one('res.country',"Country of Destination")
    country_last_export = fields.Many2one('res.country',"Country of last (re)Exportation")
    last_reexport_date = fields.Date(string='Permit Validity')
    permit_number_ir = fields.Char("Permit Number", tracking=True)
    permit_number_ir_date = fields.Date(string='Dated')
    permit_claim = fields.Selection([('active','Active'),('claimed','Claimded')], string='Permit Claim', tracking=True)
    claim_notes = fields.Text("Claim Notes", tracking=True)
    special_conditions = fields.Text("Special Conditions", tracking=True)
    exporter_name = fields.Char("Exporter Name", tracking=True)
    exporter_company = fields.Char("Exporter Company", tracking=True)

    security_stamp_no = fields.Char("Security Stamp details", tracking=True)
    permit_number_lir = fields.Char("Permit Number Last ", tracking=True)


    qr_image = fields.Binary("QR Code", attachment=False, tracking=True)
    qr_in_report = fields.Boolean('Show QR in Report')


    # @api.multi
    def print_permit(self):
        
        this = self.browse(self.ids[0])
        current_user = self.env['res.users'].browse(self._uid)

        values = {
                'type': 'ir.actions.report',
                'report_name': 'ecites.permit1',
                'report_type': 'pentaho',
                'datas': {
                        'output_type': 'pdf',
                        'variables': {
                            'ids': self.id,
                        }
                    },
                }   

        #raise osv.except_osv('Test',values )
        return values




class eCitesApplicationLine(models.Model):
    _name = 'ecites.application.line'



    @api.onchange('s_category')
    def onchange_s_category(self):
        self.s_name = False
        return {'domain': {'s_name': [('s_type', '=', self.s_category)]}}


    @api.onchange('s_name')
    def onchange_s_name(self):
        self.s_common_name = self.s_name.s_english_name1
        self.cites_appendix = self.s_name.s_current_listing
        # self.price = self.s_name.product_id.list_price

    @api.onchange('quantity')
    def onchange_quantity(self):
        self.line_total = self.quantity*self.price


    application_id = fields.Many2one('ecites.application', "Application Id", ondelete='cascade')

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
