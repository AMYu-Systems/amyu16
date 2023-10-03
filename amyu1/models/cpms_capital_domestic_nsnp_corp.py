from odoo import models, fields


class CapitalDomesticNsnp(models.Model):
    _name = 'capital.domestic.nsnp'
    _description = "Capital Domestic NSNP"

    name = fields.Float(string="Capital Contribution Amount")
    capital_domestic_id = fields.Many2one(comodel_name='client.profile',
                                          string="Capital Contribution Amount")
