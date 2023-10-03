from odoo import models, fields


class CapitalForeignNsnp(models.Model):
    _name = 'capital.foreign.nsnp.corp'
    _description = "Capital Foreign NSNP"

    name = fields.Float(string="Assigned Capital Amount")
    capital_foreign_nsnp_id = fields.Many2one(comodel_name='client.profile',
                                          string="Assigned Capital Amount")
