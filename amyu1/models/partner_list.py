from odoo import models, fields


class PartnerTags(models.Model):
    _name = 'partner.tags'
    _rec_name = "cluster_id"
    _description = "Partner Tags"

    cluster_id = fields.Char(string="Manager")
    active = fields.Boolean(string="Active", default=True)
