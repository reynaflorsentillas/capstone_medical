from odoo import models, fields

class MedicalSpecialty(models.Model):
    _name = 'medical.specialty'
    
    code = fields.Char(required=True, transalate=True)
    name = fields.Char(string='Specialty', required=True, transalate=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Name must be unique!'),
    ]
