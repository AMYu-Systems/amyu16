from odoo import fields, models, api


class ARJournal(models.Model):
    _name = 'soa.ar.journal'
    _description = "AR Journal of Client"
    _sql_constraints = [
        (
            'unique_client_id',
            'unique(client_id)',
            'Can\'t have duplicate journal for clients.'
        )
    ]

    client_id = fields.Many2one(string="Client Name", comodel_name='client.profile', required=True)

    # # use this to change value in view
    # view_initial_balance = fields.Float('Initial Balance')
    # # do not show in view
    # initial_balance = fields.Float()
    
    balance = fields.Float(compute='_compute_balance', store=False)

    accounts_receivable_ids = fields.One2many(comodel_name='soa.accounts.receivable', inverse_name='ar_journal_id')
    payments_collection_ids = fields.One2many(comodel_name='soa.payments.collection', inverse_name='ar_journal_id')
    ar_ids_count = fields.Integer()
    pc_ids_count = fields.Integer()

    name = fields.Char(string="Name", compute="_compute_name")

    @api.depends("client_id")
    def _compute_name(self):
        for record in self:
            record.name = record.client_id.name

    def _compute_balance(self):
        for record in self:
            ar_amt, pc_amt = self._get_ar_pc_amount(record=record)
            record.balance = ar_amt - pc_amt

    # @api.onchange('view_initial_balance')
    # def _onchange_initial_balance(self):
    #     self.balance -= self.initial_balance
    #     self.balance += self.view_initial_balance
    #     self.initial_balance = self.view_initial_balance

    def new_billing(self, billing):
        # self.balance = billing.amount # note that billing amount is already prev.amt + servs.amt
        self.ar_ids_count += 1
        ar = self.env['soa.accounts.receivable'].create({
            'ar_journal_id': self.id,
            'billing_id': billing.id,
            'journal_index': self.ar_ids_count
        })
        self.accounts_receivable_ids = [(4, ar.id)]  # this syntax, with 4, means add apparently

    def new_collection(self, collection, billing):
        # self.balance -= collection.amount
        self.pc_ids_count += 1
        # ar = self.env['soa.accounts.receivable'].search([('billing_id','=',billing.id)], limit=1)
        ar = self.accounts_receivable_ids[-1]
        pc = self.env['soa.payments.collection'].create({
            'ar_journal_id': self.id,
            'collection_id': collection.id,
            'related_ar_record': ar.id,
            'journal_index': self.pc_ids_count
        })
        self.payments_collection_ids = [(4, pc.id)]

    def new_manual_posting(self, collection, manual_amount):
        # self.balance -= manual_amount
        self.pc_ids_count += 1
        ar = self.accounts_receivable_ids[-1]
        pc = self.env['soa.payments.collection'].create({
            'ar_journal_id': self.id,
            'collection_id': collection.id,
            'related_ar_record': ar.id,
            'journal_index': self.pc_ids_count,
            'amount': manual_amount,
            'manual_amount': manual_amount,
            'manual_posting': True,
        })
        self.payments_collection_ids = [(4, pc.id)]
        return pc

    def void_billing(self, billing):
        ar = self.env['soa.accounts.receivable'].search([('billing_id', '=', billing.id)], limit=1)
        if ar:
            self.accounts_receivable_ids = [(2, ar.id)]  # this syntax, with 2, means delete apparently
            self.ar_ids_count -= 1
        # self.balance = billing.previous_amount if not len(self.accounts_receivable_ids) == 0 else 0

    def recalculate(self):
        # self.initial_balance = self.view_initial_balance
        ar_amt, pc_amt = self._get_ar_pc_amount()
        self.balance = ar_amt - pc_amt
    
    def _get_ar_pc_amount(self, record=None):
        record = self if not record else record
        ar = record.accounts_receivable_ids[-1] if len(record.accounts_receivable_ids) > 0 else None
        if ar:
            pcs = self.env['soa.payments.collection'].search([
                ('ar_journal_id', '=', record.id),
                ('related_ar_record', '=', ar.id),])
            ar_amt = ar.amount
        else:
            pcs = self.env['soa.payments.collection'].search([('ar_journal_id', '=', record.id)])
            ar_amt = 0
        pc_amt = 0
        for pc in pcs:
            pc_amt += pc.amount
        return ar_amt, pc_amt
    
    # Most recent billing record
    most_recent_billing_id = fields.Many2one(comodel_name='bcs.billing', compute='_compute_most_recent_billing', store=True)
    # Collection records for most recent billing
    # recent_billing_collection_ids = fields.Many2many(comodel_name='bcs.collection')
        
    @api.depends('accounts_receivable_ids')
    def _compute_most_recent_billing(self):
        for record in self:
            ar_ids = record.accounts_receivable_ids
            if len(ar_ids) <= 0: continue
            record.most_recent_billing_id = ar_ids[-1].billing_id
            
    def get_most_recent_billing(self):
        return self.most_recent_billing_id
    
    # @api.depends('payments_collection_ids', 'most_recent_billing_id')
    # def _compute_recent_billing_collections(self):
    #     for record in self:
    #         mrb_id = record.most_recent_billing_id
    #         pc_ids = record.payments_collection_ids
    #         collection_ids = []
    #         for pc_id in pc_ids:
    #             if pc_id.related_ar_record.billing_id == mrb_id.id:
    #                 pc_id.collection_id

    """ FOR DEBUGGING PURPOSES ONLY """
    def reset_journal(self):
        self.accounts_receivable_ids = [(6, 0, [])]
        self.payments_collection_ids = [(6, 0, [])]
        self.ar_ids_count = 0
        self.pc_ids_count = 0

    def open_rec(self):
        return {
            'name': 'AR Journal | ' + self.client_id.name,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'soa.ar.journal',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'flags': {'form': {'action_buttons': True}}
        }
