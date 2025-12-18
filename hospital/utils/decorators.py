from functools import wraps
from odoo import fields, api


def compute_age(dob_field="dob", age_field="age"):
    """
    Custom decorator to compute age from dob.
    - Uses @api.depends so Odoo ORM knows to trigger recompute
    """
    def decorator(func):
        @api.depends(dob_field)
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            today = fields.Date.today()
            for rec in self:
                dob = rec[dob_field]
                if dob:
                    rec[age_field] = (today - dob).days // 365
                else:
                    rec[age_field] = 0
        return wrapper
    return decorator

setattr(api,"compute_age", compute_age)
