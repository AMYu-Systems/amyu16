from odoo import models, fields


class GeneralProfessionalPartnership(models.Model):
    _name = 'general.professional.partnership'
    _description = "General Professional Partnership"

    name = fields.Char(string="Managing Partner")
    partner = fields.Char(string="Partner")
    client_profile_id = fields.Many2one(comodel_name='client.profile', string="Professional")
