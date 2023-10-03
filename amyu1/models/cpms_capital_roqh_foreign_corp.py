from odoo import models, fields


class CapitalRoqhForeignCorp(models.Model):
    _name = 'capital.roqh.foreign.corp'
    _description = "Capital ROQH Foreign Corporation"

    name = fields.Float(string="Assigned Capital Amount")
    capital_roqh_foreign_corp_id = fields.Many2one(comodel_name='client.profile',
                                                   string="Assigned Capital Amount")
