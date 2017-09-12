from __future__ import division

import odoo.http as http
from odoo.http import request
import werkzeug


class AppointmentOnline(http.Controller):

    @http.route('/page/appointment', type='http', auth="public", website=True)
    def index(self, **kw):
        Physicians = http.request.env['medical.physician']
        Consultations = http.request.env['medical.physician.services']
        return http.request.render('medical_website.appointmentonline', {
            'physicians': Physicians.search([]),
            'consultations': Consultations.search([])
        })

    @http.route('/page/appointment/create', type='http', auth="public", methods=['POST'], website=True)
    def create_appointment(self, new_patient, patient_email, patient_phone, physician_id, consultations, appointment_date, **post):
        # raise ValueError("ERROR %s" % appointment_date)
        physician = request.env['medical.physician'].search([('id', '=', physician_id)])
        physician_services = request.env['medical.physician.services'].search([('id', '=', consultations)])
        hours = physician_services.service_duration_hours
        minutes = physician_services.service_duration_minutes
        duration = float(int(hours) + int(minutes) / 60)
        new_appointment_request = request.env['medical.appointment'].create({
            'is_new_patient': True,
            'new_patient': new_patient,
            'patient_email': patient_email,
            'patient_phone': patient_phone,
            'physician_id': physician.id,
            'specialty_id': physician.specialty_id.id,
            'institution_id': physician.institution_id.id,
            'consultations': physician_services.id,
            'appointment_date': appointment_date,
            'duration': duration,
        })
        return werkzeug.utils.redirect("/page/appointment/create/thankyou")

    @http.route('/page/appointment/create/thankyou', type='http', auth="public", website=True)
    def thankyou(self, **kw):
        return http.request.render('medical_website.thankyou', {})