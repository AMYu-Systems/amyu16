from odoo import models, fields


class CorporateOfficer(models.Model):
    _name = "corporate.officer"
    _description = "Corporate Officers"

    name = fields.Char(string='Name', required=True)
    position = fields.Char(string='Position')
    client_profile_ids = fields.Many2one(comodel_name='client.profile', string="Partner")
