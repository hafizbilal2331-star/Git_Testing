from odoo import http
from odoo.http import request

class HospitalWebsite(http.Controller):

    @http.route('/patients', type='http', auth='public', website=True)
    def list_patients(self, **kwargs):
        patients = request.env['hospital.patient'].sudo().search([])
        return request.render('hospital.patients_list', {
            'patients': patients
        })

    @http.route('/patients/<model("hospital.patient"):patient>', type='http', auth='public', website=True)
    def patient_detail(self, patient):
        return request.render('hospital.patient_detail', {
            'patient': patient
        })

