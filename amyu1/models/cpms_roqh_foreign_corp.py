from odoo import models, fields


class RoqhForeignCorp(models.Model):
    _name = 'roqh.foreign.corp'
    _description = "ROQH of Foreign Corp"

    name = fields.Char(string="Country Manager")
    asst_manager = fields.Char(string="Asst.Country Manager")
    client_profile_id = fields.Many2one(comodel_name='client.profile', string="ROHQ")
