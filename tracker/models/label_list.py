from odoo import models, fields


class LabelList(models.Model):
    _name = 'label.list'
    _description = "Label Selection"

    name = fields.Selection(string="Label",
                            selection=[('checked', 'Checked'), ('review', 'Review'), ('approved', 'Approved'),
                                       ('proofread', 'Proofread')])
    active = fields.Boolean(string="Active")
    label_id = fields.Many2one(string="Label", comodel_name='main.view')
