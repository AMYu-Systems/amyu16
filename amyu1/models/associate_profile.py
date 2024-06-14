from odoo import fields, models


class AssociateProfile(models.Model):
    _name = 'associate.profile'
    _description = "Associate Profile"
    _rec_name = 'team_id'

    user_id = fields.Many2one(string="User", comodel_name='hr.employee')
    supervisor_id = fields.Many2one(string="Supervisor", comodel_name='res.users')
    manager_id = fields.Many2one(string="Manager", comodel_name='res.users')
    team_id = fields.Many2one(comodel_name='team.department', string="Team")
    cluster_id = fields.Many2one(comodel_name='cluster.department', string="Department")
    image = fields.Image(string="Image")
    client_profile_ids = fields.One2many(string="Clients", comodel_name='client.profile',
                                         inverse_name="team_id")
    job_id = fields.Many2one(string="Job Position", comodel_name='job.title')
    lead_partner_id = fields.Many2one(string="Partner", comodel_name='res.users')
