from odoo import models, fields


class CapitalGeneralPartnership(models.Model):
    _name = 'capital.general.partnership'
    _description = "Capital General Partnership"

    name = fields.Char(string="Partner")
    capital_contribution_amount = fields.Float(string="Capital Contribution Amount")
    capital_general_partner_id = fields.Many2one(comodel_name='client.profile',
                                                 string="Capital Contribution Amount")
