from odoo import fields, models


class AssociatesProfile(models.Model):
    _name = 'associates.profile'
    _description = "Associate Profile"

    name = fields.Char(string="Associates")
    associates_image = fields.Image(string="Pictures")
    client_profile_ids = fields.One2many(string="Clients", comodel_name="client.profile",
                                         inverse_name="associate_id",readonly=True)
