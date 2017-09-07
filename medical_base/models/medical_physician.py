# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.addons.medical.medical_constants import days, hours, minutes

import logging
_logger = logging.getLogger(__name__)


class MedicalPhysicianServices(models.Model):
    '''
    Services provided by the Physician on a specific medical center.

    A physician could have "surgeries" on one center but only
    "general consultation" in another center,
    or the same service with different prices for each medical center.
    That's the reason to link this to res.partner instead of
    medical_physician.
    '''
    _name = 'medical.physician.services'
    _description = 'Physician Services'
    _inherits = {'product.product': 'product_id', }

    product_id = fields.Many2one('product.product', 'Related Product', required=True, ondelete='restrict', help='Product related information for Appointment Type')
    physician_id = fields.Many2one('medical.physician', 'Physician', required=True, select=1, ondelete='cascade')
    # service_duration = fields.Selection(minutes, string='Duration')
    service_duration_hours = fields.Selection(hours, string='Duration Hours')
    service_duration_minutes = fields.Selection(minutes, string='Duration Minutes')

class MedicalPhysicianScheduleTemplate(models.Model):
    '''
    Available schedule for the Physiscian.

    ie: A physician will be able to say, in this schedule on this days.

    The objective is to show the availbles spaces for every physiscian
    '''
    _name = 'medical.physician.schedule.template'
    physician_id = fields.Many2one('medical.physician', 'Physician', required=True, select=1, ondelete='cascade')
    day = fields.Selection(days, string='Day', sort=False)
    start_hour = fields.Selection(hours, string='Start Hour')
    start_minute = fields.Selection(minutes, string='Start Minute')
    end_hour = fields.Selection(hours, string='End Hour')
    end_minute = fields.Selection(minutes, string='End Minute')
    duration = fields.Selection(minutes, string='Duration')

class MedicalPhysician(models.Model):
    _name = 'medical.physician'
    _inherits = {'res.partner': 'partner_id', }

    # id = fields.Integer('ID', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Related Partner', required=True, ondelete='cascade', help='Partner related data of the physician')
    code = fields.Char(size=256, string='ID')
    specialty_id = fields.Many2one('medical.specialty', string='Specialty', required=True, help='Specialty Code')
    institution_id = fields.Many2one(comodel_name='res.partner', domain="[('is_institution', '=', True)]", string='Medical Center')
    info = fields.Text(string='Extra info')
    active = fields.Boolean('Active', default=True, help='If unchecked, it will allow you to hide the physician without removing it.')
    schedule_template_ids = fields.One2many('medical.physician.schedule.template', 'physician_id', 'Related Schedules')
    service_ids = fields.One2many('medical.physician.services', 'physician_id', 'Physician Services')

    # OVERRIDE FIELD 
    # parent_id = fields.Many2one(domain="[('is_institution', '=', True)]", string="Medical Center")

    @api.model
    def default_get(self, fields):
        res = super(MedicalPhysician, self).default_get(fields)
        if 'is_doctor' in fields:
            res.update({'is_doctor': True})
        if 'supplier' in fields:
            res.update({'supplier': True})
        if 'active' in fields:
            res.update({'active': True})
        return res

    @api.model
    def create(self, vals,):
        groups_proxy = self.env['res.groups']
        group_ids = groups_proxy.search([('name', '=', 'Medical Doctor')])
        vals['groups_id'] = [(6, 0, group_ids)]
        return super(MedicalPhysician, self).create(vals)
