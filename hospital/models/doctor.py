from odoo import models, fields


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Doctors'


    name = fields.Char(string="Name", )
    address = fields.Text(string='Address')
    phone = fields.Integer(string='Phone No')
    dob = fields.Date(string="Date of Birth")
    patient_ids= fields.One2many('hospital.patient','doctor_id',string="")
    appointment_count = fields.Integer(string='Appointment Count', compute='compute_appointment_count')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender")




    # this func is for smart button
    def compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('doctor_id', '=', rec.id)])
            rec.appointment_count = appointment_count
