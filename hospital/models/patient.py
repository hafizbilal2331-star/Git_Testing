from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import date
from ..utils.decorators import compute_age


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['hospital.person.mixin']
    _description = 'Patient'

    name = fields.Char(string="Full Name", required=True)
    form_no = fields.Char(string="Form No", required=True, unique=True)
    # address = fields.Text(string='Address')
    age = fields.Integer(string='Age' , compute='_compute_age', store=True, readonly=True)
    dob = fields.Date(string="Date of Birth")
    # gender = fields.Selection([
    #     ('male', 'Male'),
    #     ('female', 'Female'),
    #     ('other', 'Other')
    # ], string="Gender")
    appointment_history = fields.Text(string="Appointment History")
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")
    appointment_ids=fields.One2many('hospital.appointment','patient_id',string="Appointments")
    appointment_count = fields.Integer(string='Appointment Count', compute='compute_appointment_count')
    blood_group = fields.Selection([
        ('O-', 'O-'),
        ('O+', 'O+'),
        ('A-', 'A-'),
        ('A+', 'A+'),
        ('B-', 'B-'),
        ('B+', 'B+'),
        ('AB-', 'AB-'),
        ('AB+', 'AB+')
    ], string="Blood group")

    # these 2 func is for smart buttons
    def compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            rec.appointment_count = appointment_count

    def action_open_appointments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'hospital.appointment',
            'domain': [('patient_id', '=', self.id)],
            'view_mode': 'list,form',
            'target': 'current',

        }


    # Custom decorator
    @api.compute_age("dob", "age")
    def _compute_age(self):
        pass

    @api.constrains('name')
    def check_name(self):
        for rec in self:
            patients = self.env['hospital.patient'].search([('name', '=', rec.name), ('id', '!=', rec.id)])
            if patients:
                raise ValidationError(("Name %s Already Exists" % rec.name))

    @api.ondelete(at_uninstall=False)
    def check_appointment(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(("You can't delete a patient with appointments"))

    @api.onchange('dob')
    def _onchange_dob(self):
        if self.dob:
            today = date.today()
            if self.dob > today:
                return {
                    'warning': {
                        'title': 'Invalid Date of Birth',
                        'message': 'Date of Birth cannot be in the future!'
                    }
                }
            self.age = today.year - self.dob.year - (
                (today.month, today.day) < (self.dob.month, self.dob.day)
            )
        else:
            self.age = 0


    @api.onchange('form_no')
    def _onchange_form_no(self):
        if self.form_no:
            existing = self.env['hospital.patient'].search([('form_no', '=', self.form_no)], limit=1)
            if existing and existing.id != self.id:
                return {
                    'warning': {
                        'title': 'Duplicate Form No',
                        'message': 'This Form No already exists. Please enter a unique one.'
                    }
                }
    @api.onchange('doctor_id')
    def _onchange_doctor_id(self):
        if self.doctor_id:
            gender = dict(self.doctor_id._fields['gender'].selection).get(self.doctor_id.gender, '')
            self.appointment_history = f"Consulting with {self.doctor_id.name} ({gender})."