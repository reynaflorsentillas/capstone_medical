from __future__ import division

from odoo import api, models, fields, _
from odoo import SUPERUSER_ID
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

import time
from datetime import datetime, timedelta

import math

from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class MedicalAppointmentStage(models.Model):
    _name = "medical.appointment.stage"
    _description = "Stage of Appointment"
    _rec_name = 'name'
    _order = "sequence"

    name = fields.Char(string='Stage Name', size=64, required=True, translate=True)
    sequence = fields.Integer(string='Sequence', help="Used to order stages. Lower is better.", default=1)
    requirements = fields.Text(string='Requirements')
    fold = fields.Boolean(string='Folded in Kanban View', help='This stage is folded in the kanban view when there are no records in that stage to display.', default=False)
    is_default = fields.Boolean(string='Default?', help="If checked, this stage will be selected when creating new appointments.")


class MedicalAppointment(models.Model):
    _name = 'medical.appointment'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = "Medical Appointment"

    def _get_default_stage_id(self):
        # """ Gives default stage_id """
        stage_ids = self.env['medical.appointment.stage'].search([('is_default', '=', True)], order='sequence', limit=1)
        if stage_ids:
            return stage_ids[0]
        return False

    def _read_group_stage_ids(self, stages, domain, order):
        order = stages._order
        search_domain = []
        # perform search
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        result = stages.browse(stage_ids)
        return result

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            name = '[%s] %s %s' % (rec.name, rec.patient_id.name, rec.appointment_date)
            res.append((rec.id, name))
        return res

    name = fields.Char(string='Appointment ID', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    STATES = {'draft': [('readonly', False)]}

    user_id = fields.Many2one('res.users', 'Responsible', readonly=True, default=lambda self: self.env.user, states=STATES)
    patient_id = fields.Many2one('medical.patient', string='Patient', required=False, select=True, help='Patient Name')
    # patient_id = fields.Many2one('medical.patient', string='Patient', select=True, help='Patient Name')
    patient_email = fields.Char(string='Email')
    patient_phone = fields.Char(string='Phone')
    appointment_date = fields.Datetime(string='Date and Time', required=True, default=fields.Datetime.now)
    date_end = fields.Datetime(string='End Date and Time', compute='compute_appointment_date_end', store=True)
    duration = fields.Float('Duration', default=01.00, required=True, help='The duration will be how long the appointment will take. Should be in format: hour:minute.')
    physician_id = fields.Many2one('medical.physician', string='Physician', select=True, required=True, help='Physician\'s Name')
    alias = fields.Char(size=256, string='Alias')
    comments = fields.Text(string='Comments')
    appointment_type = fields.Selection([('ambulatory', 'Ambulatory'), ('outpatient', 'Outpatient'),('inpatient', 'Inpatient'), ], string='Type', default='outpatient')
    institution_id = fields.Many2one('res.partner', string='Health Center', help='Medical Center', domain="[('is_institution', '=', True)]")
    consultations = fields.Many2one('medical.physician.services', string='Consultation Services', help='Consultation Services', domain="[('physician_id', '=', physician_id)]")
    # consultations = fields.Many2one(string='Consultation Service', comodel_name='product.product', required=True, ondelete="cascade", domain="[('type', '=', 'service')]")
    urgency = fields.Selection([('a', 'Normal'), ('b', 'Urgent'), ('c', 'Medical Emergency'), ], string='Urgency Level', default='a')
    specialty_id = fields.Many2one('medical.specialty', string='Specialty', help='Medical Specialty / Sector')
    stage_id = fields.Many2one('medical.appointment.stage', 'Stage', track_visibility='onchange', default=lambda self: self._get_default_stage_id(), group_expand='_read_group_stage_ids')
    current_stage = fields.Integer(related='stage_id.sequence', string='Current Stage')
    history_ids = fields.One2many('medical.appointment.history', 'appointment_id', 'History lines')

    @api.multi
    @api.onchange('consultations')
    def compute_appointment_duration(self):
        for record in self:
            if record.consultations:
                hours = record.consultations.service_duration_hours
                minutes = record.consultations.service_duration_minutes
                duration = float(int(hours) + int(minutes) / 60)
                record.duration = duration

    @api.multi
    @api.onchange('patient_id')
    def set_patient_details(self):
        for record in self:
            if record.patient_id:
                record.patient_email = record.patient_id.email
                record.patient_phone = record.patient_id.phone

    @api.multi
    @api.depends('appointment_date', 'duration')
    def compute_appointment_date_end(self):
        for record in self:
            duration = record.duration
            factor = duration < 0 and -1 or 1    
            val = abs(duration)    
            hour, minute = (factor * int(math.floor(val)), int(round((val % 1) * 60)))

            appointment_date = datetime.strptime(record.appointment_date, '%Y-%m-%d %H:%M:%S')
            
            date_end = appointment_date + timedelta(hours=hour, minutes=minute)
            record.date_end = date_end

    def _get_appointments(self, physician_ids, institution_ids, date_start, date_end):
        # """ Get appointments between given dates, excluding pending review and cancelled ones """

        pending_review_id = self.env['ir.model.data'].get_object_reference('medical_base', 'stage_appointment_in_review')[1]
        cancelled_id = self.env['ir.model.data'].get_object_reference('medical_base', 'stage_appointment_canceled')[1]
        
        domain = [('physician_id', 'in', physician_ids),
                  ('date_end', '>', date_start),
                  ('appointment_date', '<', date_end),
                  ('stage_id', 'not in', [pending_review_id, cancelled_id])]

        if institution_ids:
            domain += [('institution_id', 'in', institution_ids)]

        result = self.search(domain)

        return result

    def _set_clashes_state_to_review(self, physician_ids, institution_ids, date_start, date_end):
        review_stage_id = self.env['ir.model.data'].get_object_reference('medical_base', 'stage_appointment_in_review')[1]
        if not review_stage_id:
            raise UserError(_('No default stage defined for review'))
        current_appointments = self._get_appointments(physician_ids, institution_ids, date_start, date_end)
        if current_appointments:
            current_appointments.write({'stage_id': review_stage_id})

    @api.model
    def create(self, values):
        if values.get('name', 'New') == 'New':
            values['name'] = self.env['ir.sequence'].next_by_code('medical.appointment') or 'New'

        result = super(MedicalAppointment, self).create(values)

        # CREATE HISTORY RECORD
        appointment_history = self.env['medical.appointment.history'].create({
            'date' : time.strftime('%Y-%m-%d %H:%M:%S'),
            'appointment_id': result.id,
            'action' : "----  Created  ----"
        }) 

        return result

    @api.onchange('physician_id')
    def _get_physician_specialty(self):
        for r in self:
            r.specialty_id = r.physician_id.specialty_id
            r.institution_id = r.physician_id.institution_id

    # TO BE MOVED TO VISIT MODULE
    @api.multi
    def action_create_visit(self):
        for record in self:
            if record.appointment_type == 'outpatient':
                visit_id = self.env['medical.visit'].create({
                    'appointment_id': self.id,
                    'patient_id': self.patient_id.id,
                    'physician_id': self.physician_id.id,
                    'institution_id': self.institution_id.id,
                    'urgency': self.urgency,
                    'consultations': self.consultations.id,
                    'scheduled_start': self.appointment_date,
                })

                self.stage_id = 3

                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Patient Visit',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'medical.visit',
                    'res_id': visit_id.id,
                    'view_id': self.env.ref('medical.medical_visit_form').id,
                    'target': 'current',
                }

    # TO BE MOVED TO HOSPITALIZATION MODULE
    @api.multi
    def action_create_hospitalization(self):
        for record in self:
            if record.appointment_type == 'inpatient':
                hospitalization_id = self.env['medical.patient.hospitalization'].create({
                    ''
                })
            return True

    def write(self, values):
        context = self.env.context.copy()
        original_values = self.read(['physician_id', 'institution_id', 'appointment_date', 'date_end', 'duration'])[0]
        date_start = values.get('appointment_date', original_values['appointment_date'])
        
        result = super(MedicalAppointment, self).write(values)

        # stage change: update date_last_stage_update
        if 'stage_id' in values:
            appointment_history = self.env['medical.appointment.history']
            stage_id = self.env['medical.appointment.stage'].search([('id', '=', values['stage_id'])])
            val_history = {
                'action': "----  Changed to {0}  ----".format(stage_id.name),
                'appointment_id': self.id,
                'date': time.strftime('%Y-%m-%d %H:%M:%S'),
            }
            appointment_history.create(val_history)

            user_record = self.env['res.users'].browse(SUPERUSER_ID)
            lang_id = self.env['res.lang'].search([('code', '=', user_record.lang)])
            localized_datetime = datetime.strptime(date_start, DEFAULT_SERVER_DATETIME_FORMAT)
            context.update({'appointment_date': localized_datetime.strftime(lang_id.date_format), 'appointment_time': localized_datetime.strftime(lang_id.time_format)})

            mail_template_name = None

            if stage_id.name == 'Pending Review':
                mail_template_name = 'email_template_appointment_pending_review'
            elif stage_id.name == 'Confirm':
                mail_template_name = 'email_template_appointment_confirmation'
            elif stage_id.name == 'Canceled':
                mail_template_name = 'email_template_appointment_canceled'

            if mail_template_name:
                template_res = self.env['mail.template']
                imd_res = self.env['ir.model.data']
                template_id = imd_res.get_object_reference('medical_base', mail_template_name)[1]
                template = template_res.browse(template_id)
                template.with_context(context).send_mail(self.id, force_send=True)

        return result

class MedicalAppointmentHistory(models.Model):
    _name = 'medical.appointment.history'
    _description = "Medical Appointment History"

    date = fields.Datetime(string='Date and Time')
    name = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    action = fields.Text(string='Action')
    appointment_id = fields.Many2one('medical.appointment', string='History', ondelete='cascade')
