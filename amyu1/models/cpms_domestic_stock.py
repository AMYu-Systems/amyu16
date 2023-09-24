from odoo import models, fields


class DomesticStock(models.Model):
    _name = 'domestic.stock'
    _description = "Domestic Stock"

    name = fields.Char(string="Chairman of the BOD")
    president = fields.Char(string="President/CEO")
    treasurer = fields.Char(string="Treasurer/CFO")
    corporate_secretary = fields.Char(string="Corporate Secretary")
    vice_chairman = fields.Char(string="Vice-Chairman of the BOD")
    asst_treasurer = fields.Char(string="Asst.Treasurer")
    asst_corp_secretary = fields.Char(string="Asst.Corporate Secretary")
    domestic_stock_id = fields.Many2one(comodel_name='client.profile', string="Domestic Stock")
