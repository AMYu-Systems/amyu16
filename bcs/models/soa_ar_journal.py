from odoo import fields, models, api


class ARJournal(models.Model):
    _name = 'soa.ar.journal'
    _description = "AR Journal of Client"
    name = fields.Text(string="Name")
    
    client = fields.Text()
    initial_balance = fields.Float()
    balance = fields.Float()
    
    accounts_receivable_ids = fields.Many2many('soa.accounts.receivable')
    payments_collection_ids = fields.Many2many('soa.payments.collection')
    ar_ids_count = fields.Integer()
    pc_ids_count = fields.Integer()

    @api.depends("client")
    def _compute_name(self):
        for record in self:
            record.name = record.client
            
    def add_accounts_receivable(self, ar):
        self.accounts_receivable_ids.add(ar)
        self.balance = ar.amount
        self.ar_ids_count += 1
    
    def add_payments_collection(self, pc):
        self.payments_collection_ids.add(pc)
        self.balance = pc.amount
        self.pc_ids_count += 1
    
    def set_initial_balance(self, initial):
        if self.balance != 0:
            return
        self.initial_balance = initial
        
    def recalculate(self):
        self.balance = 0
        # add = sum ( self.accounts_receivable_id.all )
        # sub = sum ( self.payments_collection_ids.all )
        # self.balance = add - sub
        
    def new_billing(self):
        view_tree = self.env.ref('bcs.soa_ar_journal_view_tree').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Name',
            'view_mode': 'tree',
            'res_model': 'bcs.billing',
            'view_id': view_tree,
            'domain': [()],
            'context': "{'create': False}"
        }
    