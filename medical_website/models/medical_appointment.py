from odoo import api, models, fields, _

class MedicalAppointment(models.Model):
    _inherit = 'medical.appointment'

    # Appointment Online
    is_new_patient = fields.Boolean(string='Is New Patient?')
    new_patient = fields.Char(string='New Patient')