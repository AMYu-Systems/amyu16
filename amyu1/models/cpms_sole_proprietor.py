from odoo import models, fields


class SoleProprietor(models.Model):
    _name = 'sole.proprietor'
    _description = "Sole Proprietor"

    name = fields.Char(string='Proprietor/Proprietress', required=True)
    client_profile_id = fields.Many2one(comodel_name='client.profile', string="Proprietor/Proprietress")
