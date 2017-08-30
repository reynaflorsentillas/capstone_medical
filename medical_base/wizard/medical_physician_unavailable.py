
from odoo import models, fields

import logging
_logger = logging.getLogger(__name__)

class MedicalPhysicianUnavailableWizard(models.TransientModel):
    _name = 'medical.physician.unavailable.wizard'
    _description = 'Medical Physician Unavailable Wizard'

    physician_id = fields.Many2one('medical.physician', 'Physician', required=True)
    date_start = fields.Datetime(string='Start', required=True, default=fields.Datetime.now)
    date_end = fields.Datetime(string='End', required=True, default=fields.Datetime.now)
    institution_id = fields.Many2one('res.partner', 'Medical Center', select=1, domain="[('is_institution', '=', True), ]")

    def action_cancel(self):
        return {'type': 'ir.actions.act_window_close'}

    def action_set_unavailable(self):
        # if not ids:
        #     return {}

        appointment_proxy = self.env['medical.appointment']

        physician_id = self.physician_id.id
        institution_id = self.institution_id.id
        if institution_id:
            institution_ids = [institution_id]
        else:
            institution_ids = []

        date_start = self.date_start
        date_end = self.date_end

        # appointment_proxy._remove_empty_clashes([physician_id], institution_ids, date_start, date_end)
        _logger.info('KONICHIWA')
        _logger.info(physician_id)
        _logger.info(institution_ids)
        _logger.info(date_start)
        _logger.info(date_end)
        appointment_proxy._set_clashes_state_to_review([physician_id], institution_ids, date_start, date_end)

        return {'type': 'ir.actions.act_window_close'}