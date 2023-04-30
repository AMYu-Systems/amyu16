from odoo import models, fields


class CorporateOfficer(models.Model):
    _name = "corporate.officer"
    _description = "Corporate Officer"

    name = fields.Char(string='Name', required=True)
    position = fields.Char(string='Position')
    res_ids = fields.Many2one(comodel_name='res.partner', string="Partner")


