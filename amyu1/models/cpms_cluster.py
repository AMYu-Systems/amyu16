from odoo import fields, models


class ClusterDepartment(models.Model):
    _name = 'cluster.department'
    _description = "Cluster Department"

    name = fields.Char(string="Cluster")
    active = fields.Boolean(string="Active", default=True)