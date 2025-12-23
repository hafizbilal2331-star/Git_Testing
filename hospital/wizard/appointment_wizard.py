from odoo import models, fields, api


class HospitalAppointmentWizard(models.TransientModel):
    _name = 'hospital.appointment.wizard'
    _description = 'Create Appointment Wizard'

    # Pre-fill the patient if the wizard is opened from a Patient form
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('ongoing', 'Ongoing'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], default='draft',)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=True)
    date_appointment = fields.Date(string="Appointment Date", default=fields.Date.context_today)
    reason = fields.Text(string="Reason/Note")

    def action_create_appointment(self):
        """
        Clicking the button on the wizard takes data from this
        TransientModel and creates a permanent 'hospital.appointment' record.
        """
        vals = {
            'patient_id': self.patient_id.id,
            'doctor_id': self.doctor_id.id,
            'date_appointment': self.date_appointment,
            'note': self.reason,
            'state': self.status
        }

        self.env['hospital.appointment'].create(vals)

        return {'type': 'ir.actions.act_window_close'}

    @api.model
    def default_get(self, fields):
        """
        Automatically selects the correct patient if the wizard
        is opened from the Patient's form view.
        """
        res = super(HospitalAppointmentWizard, self).default_get(fields)
        if self._context.get('active_model') == 'hospital.patient':
            res['patient_id'] = self._context.get('active_id')
        return res