from odoo import api, models, fields, _

import logging
_logger = logging.getLogger(__name__)

class MedicalAppointment(models.Model):
    _inherit = 'medical.appointment'

    # Appointment Online
    is_new_patient = fields.Boolean(string='Is New Patient?')
    new_patient = fields.Char(string='New Patient')

    @api.multi
    def action_create_patient(self):
        for record in self:
            Patient = self.env['medical.patient'].create({
                'name': record.new_patient,
                'email': record.patient_email,
                'phone': record.patient_phone
            })
            record.write({'patient_id': Patient.id, 'is_new_patient': False})