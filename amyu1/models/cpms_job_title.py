from odoo import fields, models


class JobTitle(models.Model):
    _name = 'job.title'
    _description = "Job Details"

    name = fields.Char(string="Job Position")
    cluster_ids = fields.Char(string="Cluster", comodel_name='associates.profile', inverse_name="cluster_id")
