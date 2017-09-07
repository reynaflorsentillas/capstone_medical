import odoo.http as http

class AppointmentOnline(http.Controller):
    @http.route('/page/appointment', type='http', auth='public', website=True)
    
    def index(self, **kw):
        Physicians = http.request.env['medical.physician']
        Consultations = http.request.env['product.product']
        return http.request.render('medical_base.appointmentonline', {
            'physicians': Physicians.search([]),
            'consultations': Consultations.search([('type', '=', 'service')])
        })