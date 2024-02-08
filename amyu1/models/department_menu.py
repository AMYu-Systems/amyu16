from odoo import fields, models


class TeamDepartment(models.Model):
    _name = 'team.department'
    _description = "Team Department"

    name = fields.Char(string="Team")
    active = fields.Boolean(string="Active", default=True)
    team_ids = fields.One2many(string="Job", comodel_name='associate.profile', inverse_name="team_id")


class ClusterDepartment(models.Model):
    _name = 'cluster.department'
    _description = "Cluster Department"

    name = fields.Char(string="Cluster")
    active = fields.Boolean(string="Active", default=True)
    cluster_ids = fields.One2many(string="Job", comodel_name='associate.profile', inverse_name="cluster_id")


class JobTitle(models.Model):
    _name = 'job.title'
    _description = "Job Details"

    name = fields.Char(string="Work")
    active = fields.Boolean(string="Active", default=True)
    work_ids = fields.One2many(string="Job", comodel_name='associate.profile', inverse_name="work_id")
