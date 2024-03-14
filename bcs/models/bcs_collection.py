import re

from odoo import fields, models, api


class BcsCollection(models.Model):
    _name = 'bcs.collection'
    _description = "Collection"
    _rec_name = 'transaction'

    transaction = fields.Char(string="Transaction", readonly=1)

    @api.model
    def create(self, vals):
        name = re.sub(r'\W+', ' ', vals['paid_by_id'])
        name_array = name.split()
        if len(name_array) == 1:
            transaction = name_array[0][0:3]
        elif len(name_array) == 2:
            name1 = name_array[0]
            name2 = name_array[1]
            transaction = (name1[0:2] if len(name1) >= 2 else name1[0:1]) + \
                          (name2[0:2] if len(name1) == 1 else name2[0:1])
        elif len(name_array) >= 3:
            name1 = name_array[0]
            name2 = name_array[1]
            name3 = name_array[2]
            transaction = name1[0:1] + name2[0:1] + name3[0:1]
        # Compute Client ID
        transaction += "-" + self.env['ir.sequence'].next_by_code('collection.id.seq')
        vals['transaction'] = transaction
        return super(BcsCollection, self).create(vals)

    paid_by_id = fields.Many2one(comodel_name='billing.summary', string="Paid By")
    billing_ids = fields.Many2many(comodel_name='bcs.billing', string="Billing")
    collection_type = [('direct_payment', 'Direct Payment'),
                       ('consolidated', 'Consolidated Payment'),
                       ('suspense', 'Suspense Account')]
    payment_collection = fields.Selection(collection_type, default='suspense', string="Collection Type")
    collected_by = fields.Char(string="Collected By")
    date_collected = fields.Date(string="Date Collected")
    last_update = fields.Datetime(string="Last Updated")
    bank_type = [('bpi', 'BPI'),
                 ('bdo', 'BDO'),
                 ('eastwest', 'EASTWEST'),
                 ('metrobank', 'METROBANK')]
    depository_bank = fields.Selection(bank_type, default='bpi', string="Depository Bank")
    payment_method = [('check', 'Check'),
                      ('cash', 'Cash'),
                      ('online', 'Online')]
    payment_mode = fields.Selection(payment_method, default='online', string="Mode of Payment")
    bank = fields.Char(string="Bank")
    check_number = fields.Char(string="Check Number")
    check_date = fields.Date(string="Check Date")
    transaction_generated = fields.Char(string="Transaction Generated")
    transaction_date = fields.Date(string="Transaction Date")
    amount = fields.Float(string="Amount")
    remarks = fields.Text(string="Remarks")
    unissued_amount_for_ar = fields.Float(string="Unissued Amount For AR", default=0)
