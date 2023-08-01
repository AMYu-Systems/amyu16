from odoo import models, fields


class ManagerTags(models.Model):
    _name = 'manager.tags'
    _rec_name = "manager_id"
    _description = "Manager Tags"

    manager_id = fields.Char(string="Manager")
    active = fields.Boolean(string="Active", default=True)
