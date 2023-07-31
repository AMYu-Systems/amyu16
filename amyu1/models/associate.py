from odoo import fields, models


class AssociatesProfile(models.Model):
    _name = 'associates.profile'
    _description = "Associate Profile"

    name = fields.Char(string="Associates")
    associates_image = fields.Image(string="Pictures")
    associates_manager = fields.Char(string="Manager")
    associates_supervisor = fields.Char(string="Supervisor")
    associates_cluster = fields.Char(string="Cluster")
    position = fields.Char(string="Position")
    client_profile_ids = fields.One2many(string="Clients", comodel_name="client.profile",
                                         inverse_name="associate_id",readonly=True)
