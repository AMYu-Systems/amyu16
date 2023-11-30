from odoo import fields, models


class CPMSSupervisor(models.Model):
    _name = 'cpms.supervisor'
    _description = "Team Supervisor"

    name = fields.Many2one(string="Team Supervisor", comodel_name='res.users')
    user_ids = fields.Many2many(string="Related User", comodel_name='res.users')
    active = fields.Boolean(string="Active", default=True)