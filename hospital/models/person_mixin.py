from odoo import models, fields, api


class HospitalPersonMixin(models.AbstractModel):
    _name = 'hospital.person.mixin'
    _description = 'Person Mixin'

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender")

    address = fields.Text(string='Address')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')

    def action_send_email(self):
        """Shared logic: This method can be used by both Doctors and Patients"""
        print(f"Sending email to {self.email}...")