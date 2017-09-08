import odoo.http as http
# from odoo.addons.website_form.controllers.main import WebsiteForm

class AppointmentOnline(http.Controller):

    @http.route('/page/appointment', type='http', auth="public", website=True)
    def index(self, **kw):
        Physicians = http.request.env['medical.physician']
        Consultations = http.request.env['medical.physician.services']
        return http.request.render('medical_website.appointmentonline', {
            'physicians': Physicians.search([]),
            # 'consultations': Consultations.search([('type', '=', 'service')])
            'consultations': Consultations.search([])
        })
    
    # @http.route('/website_form/<string:model_name>', type='http', auth="public", methods=['POST'], website=True)
    # def website_form(self, model_name, **kwargs):
    #     if http.request.params.get('partner_email'):
    #         Partner = http.request.env['res.partner'].sudo().search([('email', '=', kwargs.get('partner_email'))], limit=1)
    #         if Partner:
    #             http.request.params['partner_id'] = Partner.id
    #     return super(AppointmentOnline, self).website_form(model_name, **kwargs)

    @http.route('/page/appointment/create', type='http', auth="public", methods=['POST'], website=True)
    def create_appointment(self, **kw):
        return request.redirect("/page/appointment/thankyou")

    @http.route('/page/appointment/thankyou', type='http', auth="public", website=True)
    def thankyou(self, **kw):
        return http.request.render('medical_website.thankyou', {})