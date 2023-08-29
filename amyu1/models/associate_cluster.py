from odoo import fields, models


class AssociateCluster(models.Model):
    _name = 'associate.cluster'
    _description = "Cluster Department"

    name = fields.Char(string="Display Cluster")
    cluster_ids = fields.One2many(string="Cluster", comodel_name='associates.profile', inverse_name="cluster_id")
