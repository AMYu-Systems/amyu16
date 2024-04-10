from odoo import models, fields


class AssociateGroup(models.Model):
    _name = 'associate.group'
    _description = "Associate Group Profile"
    _rec_name = 'supervisor_id'

    user_id = fields.Many2one(string="Associate", comodel_name='res.users')
    supervisor_id = fields.Many2one(string="Supervisor", comodel_name='res.users')
    manager_id = fields.Many2one(string="Manager", comodel_name='res.users')
    partners_id = fields.Many2one(string="Partner", comodel_name='res.users')
