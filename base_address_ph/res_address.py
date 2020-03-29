# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ResRegion(models.Model):
    _name = 'res.region'

    name = fields.Char('Region', required=True)
    code = fields.Char('Code', required=True)
    active = fields.Boolean('Active', default=True)


class ResProvince(models.Model):
    _name = 'res.province'

    name = fields.Char('Province', required=True)
    code = fields.Char('Code', required=True)
    region_id = fields.Many2one('res.region', 'Region', ondelete="set null")
    active = fields.Boolean('Active', default=True)


class ResCityMunicipality(models.Model):
    _name = 'res.citymun'

    name = fields.Char('City / Municipality', required=True)
    code = fields.Char('Code', required=True)
    province_id = fields.Many2one('res.province', 'Province', ondelete="set null")
    active = fields.Boolean('Active', default=True)



class ResBrgy(models.Model):
    _name = 'res.brgy'

    name = fields.Char('Barangay', required=True)
    code = fields.Char('Code', required=True)
    citymun_id = fields.Many2one('res.citymun', 'City / Municipality', ondelete="set null")
    active = fields.Boolean('Active', default=True)


class ResPartner(models.Model):
    _inherit = 'res.partner'


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


    street = fields.Char('House No.')
    street2 = fields.Char('Street / Subd.')
    brgy_id = fields.Many2one('res.brgy', string='Barangay')
    citymun_id = fields.Many2one('res.citymun', string='City / Municipality')
    province_id = fields.Many2one('res.province', string='Province')
    region_id = fields.Many2one('res.region', string='Region')


class ResUsers(models.Model):
    _inherit = 'res.users'



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


    brgy_id = fields.Many2one('res.brgy', related='partner_id.brgy_id', string='Barangay')
    citymun_id = fields.Many2one('res.citymun', related='partner_id.citymun_id', string='City / Municipality')
    province_id = fields.Many2one('res.province', related='partner_id.province_id', string='Province')
    region_id = fields.Many2one('res.region', related='partner_id.region_id', string='Region')
