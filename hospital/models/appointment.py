from odoo import models, fields


class HospitalPatient(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointments'
    _rec_name = 'patient_id'

    doctor_id= fields.Many2one('hospital.doctor', string="Ref", )
    patient_id = fields.Many2one('hospital.patient', string="Patient")
    date_appointment = fields.Date(string="Date")
    note = fields.Text(string="Noted")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('ongoing', 'Ongoing'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], default='draft',)


    def action_confirm(self):
     for rec in self:
        rec.state = 'confirmed'
    def action_ongoing(self):
     for rec in self:
        rec.state = 'ongoing'
    def action_done(self):
     for rec in self:
        rec.state = 'done'
    def action_cancel(self):
     for rec in self:
        rec.state = 'cancelled'
