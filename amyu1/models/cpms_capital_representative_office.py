from odoo import models, fields


class CapitalRepresentativeOffice(models.Model):
    _name = 'capital.representative.office'
    _description = "Capital Representative Office"

    name = fields.Float(string="Assigned Capital Amount")
    capital_representative_office_id = fields.Many2one(comodel_name='client.profile',
                                                       string="Assigned Capital Amount")
