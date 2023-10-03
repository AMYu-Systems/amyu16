from odoo import models, fields


class CapitalForeignCorp(models.Model):
    _name = 'capital.foreign.corp'
    _description = "Capital Foreign Corporation"

    name = fields.Float(string="Assigned Capital Amount")
    capital_foreign_corp_id = fields.Many2one(comodel_name='client.profile',
                                              string="Assigned Capital Amount")
