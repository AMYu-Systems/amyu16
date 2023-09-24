from odoo import models, fields


class CorporateOfficer(models.Model):
    _name = "corporate.officer"
    _description = "Corporate Officers"

    name = fields.Char(string='Name', required=True)
    client_profile_id = fields.Many2one(comodel_name='client.profile', string="Corporate")
