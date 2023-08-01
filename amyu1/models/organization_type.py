from odoo import models, fields


class OrganizationType(models.Model):
    _name = 'organization.type'
    _description = "Tags"

    name = fields.Char(string="Organization Type")
    active = fields.Boolean(string="Active",default=True)
