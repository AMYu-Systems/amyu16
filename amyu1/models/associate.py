from odoo import fields, models


class AssociatesProfile(models.Model):
    _name = 'associates.profile'
    _description = "Associate Profile"

    name = fields.Char()
    user_id = fields.Many2one(comodel_name='res.users', string="Associate", default=lambda self: self.env.user,
                              readonly=True)
    supervisor_id = fields.Many2one(comodel_name='res.users', string="Supervisor")
    manager_id = fields.Many2one(comodel_name='res.users', string="Manager")
    team_id = fields.Many2one(comodel_name='res.groups', string="Team")
    cluster_id = fields.Many2one(comodel_name='job.title', string="Cluster")
    image = fields.Image(string="Image")
    client_profile_ids = fields.One2many(string="Clients", comodel_name='client.profile',
                                         inverse_name="associate_id", readonly=True)
    job_title_id = fields.Many2many(comodel_name='job.title', string="Job Position")
