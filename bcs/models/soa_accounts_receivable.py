from odoo import fields, models


class AccountsReceivable(models.Model):
    _name = 'soa.accounts.receivable'
    _description = "Accounts Receivable connected to AR Journal"
    name = fields.Text(string="Name")
    
    billing_id = fields.Many2one('bcs.billing')
    ar_journal_id = fields.Many2one('soa.ar.journal')
    journal_index = fields.Integer()
    amount = fields.Float()