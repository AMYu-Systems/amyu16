from odoo import models, fields


class RepresentativeOffice(models.Model):
    _name = 'representative.office'
    _description = "Representative Office"

    name = fields.Char(string="Country Manager")
    asst_manager = fields.Char(string="Asst.Country Manager")
    representative_office_id = fields.Many2one(comodel_name='client.profile', string="Representative")
