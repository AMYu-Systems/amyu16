from odoo import models, fields


class GeneralPartnership(models.Model):
    _name = 'general.partnership'
    _description = "General Partnership"

    name = fields.Char(string="Managing Partner")
    partner = fields.Char(string="Partner")
    general_partnership_id = fields.Many2one(comodel_name='client.profile', string="General Partnership")