from odoo import fields, models


class AssociatesProfile(models.Model):
    _name = 'associates.profile'
    _description = "Associate Profile"

    name = fields.Many2one(comodel_name="res.users", string="Associate")
    supervisor_id = fields.Many2one(comodel_name="res.users", string="Supervisor")
    manager_id = fields.Many2one(comodel_name='res.users', string="Manager")
    cluster_id = fields.Many2one(comodel_name='res.groups', string="Team")
    client_profile_ids = fields.One2many(string="Clients", comodel_name="client.profile",
                                         inverse_name="associate_id", readonly=True)
    image = fields.Image(string="Image")
