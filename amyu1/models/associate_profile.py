from odoo import fields, models


class AssociateProfile(models.Model):
    _name = 'associate.profile'
    _description = "Associate Profile"
    _rec_name = 'team_id'

    user_id = fields.Many2one(string="User", comodel_name='hr.employee')
    supervisor_id = fields.Many2one(string="Supervisor", related='user_id.coach_id')
    manager_id = fields.Many2one(string="Manager", related='user_id.parent_id')
    team_id = fields.Many2one(related='user_id.coach_id', string="Team")
    cluster_id = fields.Many2one(related='user_id.department_id', string="Department")
    job_id = fields.Many2one(string="Job Position", related='user_id.job_id')
    executive_id = fields.Many2one(string="Partner", related='user_id.executive_id')
    image = fields.Image(string="Image")
    client_profile_ids = fields.One2many(string="Clients", comodel_name='client.profile',
                                         inverse_name="team_id")
