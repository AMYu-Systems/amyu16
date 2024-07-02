from odoo import fields, models


class AssociateProfile(models.Model):
    _name = 'associate.profile'
    _description = "Associate Profile"
    _rec_name = 'team_id'
    _sql_constraints = [
        (
            'unique_user_id',
            'unique(user_id)',
            'Can\'t have duplicate users.'
        )
    ]
    user_id = fields.Many2one(string="name", comodel_name='res.users', default=lambda self: self.env.user)
    users_id = fields.Many2one(string="User", comodel_name='hr.employee')
    supervisor_id = fields.Many2one(string="Supervisor", related='users_id.coach_id')
    manager_id = fields.Many2one(string="Manager", related='users_id.parent_id')
    team_id = fields.Many2one(related='users_id.coach_id', string="Team")
    cluster_id = fields.Many2one(related='users_id.department_id', string="Department")
    job_id = fields.Many2one(string="Job Position", related='users_id.job_id')
    lead_partner_id = fields.Many2one(string="Partner", related='users_id.executive_id')
    image = fields.Image(string="Image")
    client_profile_ids = fields.One2many(string="Clients", comodel_name='client.profile',
                                         inverse_name="team_id")
