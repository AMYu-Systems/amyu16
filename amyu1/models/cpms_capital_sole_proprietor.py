from odoo import models, fields


class CapitalSoleProprietor(models.Model):
    _name = 'capital.sole.proprietor'
    _description = "Capital Sole Proprietor"

    name = fields.Float(string="Capital Contribution Amount")
    capital_sole_proprietor_id = fields.Many2one(comodel_name='client.profile',
                                                 string="Capital Contribution Amount")
