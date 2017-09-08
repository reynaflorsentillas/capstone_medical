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
    def create_appointment(self, new_patient, physician_id, consultations, **post):
        new_appointment_request = request.env['medical.appointment'].create({
            'new_patient': new_patient,
            # 'physician_id': physician_id,
            # 'consultations': consultations,
        })
        return werkzeug.utils.redirect("/page/appointment/create/thankyou")

    @http.route('/page/appointment/create/thankyou', type='http', auth="public", website=True)
    def thankyou(self, **kw):
        return http.request.render('medical_website.thankyou', {})