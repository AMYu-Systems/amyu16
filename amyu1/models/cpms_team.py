from odoo import fields, models


class TeamDepartment(models.Model):
    _name = 'team.department'
    _description = "Team Department"

    name = fields.Char(string="Team")
    active = fields.Boolean(string="Active", default=True)