from odoo import models, fields 

class MedicalEthnicGroup(models.Model):
    _name = 'medical.ethnic.group'
    _description = 'Medical Ethnic Group'

    code = fields.Char(required=True, transalate=True)
    name = fields.Char(string='Ethnic Group', required=True, transalate=True)