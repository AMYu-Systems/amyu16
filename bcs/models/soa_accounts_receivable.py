from odoo import fields, models, api


class AccountsReceivable(models.Model):
    _name = 'soa.accounts.receivable'
    _description = "Accounts Receivable connected to AR Journal"
    _sql_constraints = [
        (
            'unique_billing_id',
            'unique(billing_id)',
            'Can\'t have duplicate billing_ids.'
        )
    ]
    
    billing_id = fields.Many2one(comodel_name='bcs.billing',  required=True, ondelete='cascade', readonly=True)
    ar_journal_id = fields.Many2one(comodel_name='soa.ar.journal', required=True, ondelete='cascade', readonly=True)
    client_id = fields.Many2one(related='ar_journal_id.client_id', string='Client')
    journal_index = fields.Integer( required=True, readonly=True)
    amount = fields.Float(compute='_compute_amount')

    @api.depends("billing_id.amount")
    def _compute_amount(self):
        for record in self:
            record.amount = record.billing_id.amount

    name = fields.Char(compute="_compute_name")

    @api.depends("billing_id.date_billed", "billing_id.services_id")
    def _compute_name(self):
        for record in self:
            if not record.billing_id: continue
            services = ''
            for service in record.billing_id.services_id:
                services += service.code + ', '
            services = services[:-2]
            name = f'{record.journal_index} | '
            name += record.billing_id.date_billed.strftime("%b %Y") + ' | ' + services
            previous = "{:,.2f}".format(record.billing_id.previous_amount)
            name += ' | ' + f'Previous: {previous}'
            record.name = name
