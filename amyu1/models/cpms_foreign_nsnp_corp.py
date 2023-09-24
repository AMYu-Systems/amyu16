from odoo import models, fields


class ForeignNsnpCorp(models.Model):
    _name = 'foreign.nsnp.corp'
    _description = "Branch of Foreign NSNP Corp"

    name = fields.Char(string="Country Manager")
    asst_manager = fields.Char(string="Asst.Country Manager")
    foreign_nsnp_corp_id = fields.Many2one(comodel_name='client.profile', string="Foreign NSNP")
