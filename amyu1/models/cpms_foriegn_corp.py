from odoo import models, fields


class ForeignCorp(models.Model):
    _name = 'foreign.corp'
    _description = "Branch of Foreign Corp"

    name = fields.Char(string="Country Manager")
    asst_manager = fields.Char(string="Asst.Country Manager")
    client_profile_id = fields.Many2one(comodel_name='client.profile', string="Foreign Corporation")
