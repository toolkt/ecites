# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError, AccessError, UserError
from odoo.modules.module import get_module_resource
from odoo.tools.translate import html_translate
import base64
from odoo import api, fields, models, _


class ResCountry(models.Model):
    _inherit = 'res.country'

    def search_record(self, needle=None, limit=None):
        res = []
        for rec in self.sudo().search([('name','ilike',needle)]):
            res.append({'label':rec.name,'value':rec.id})
            if len(res) == limit:
                break
        return res

class ResBrgy(models.Model):
    _inherit = 'res.brgy'

    def search_record(self, needle=None, limit=None):
        res = []
        for rec in self.sudo().search([('name','ilike',needle)]):
            res.append({'label':rec.name,'value':rec.id})
            if len(res) == limit:
                break
        return res


class ResCityMun(models.Model):
    _inherit = 'res.citymun'

    def search_record(self, needle=None, limit=None):
        res = []
        for rec in self.sudo().search([('name','ilike',needle)]):
            res.append({'label':rec.name,'value':rec.id})
            if len(res) == limit:
                break
        return res


class ResProvince(models.Model):
    _inherit = 'res.province'

    def search_record(self, needle=None, limit=None):
        res = []
        for rec in self.sudo().search([('name','ilike',needle)]):
            res.append({'label':rec.name,'value':rec.id})
            if len(res) == limit:
                break
        return res


class ResRegion(models.Model):
    _inherit = 'res.region'

    def search_record(self, needle=None, limit=None):
        res = []
        for rec in self.sudo().search([('name','ilike',needle)]):
            res.append({'label':rec.name,'value':rec.id})
            if len(res) == limit:
                break
        return res





