import re

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class BcsBilling(models.Model):
    _name = 'bcs.billing'
    _description = "Billing"
    _rec_name = 'name'
    # _rec_name = 'transaction'

    name = fields.Char(compute="_compute_name")
    @api.depends("services_id", "date_billed")
    def _compute_name(self):
        for record in self:
            services = ''
            if record.services_id:
                for service in record.services_id:
                    services += service.code + ', '
                services = services[:-2]
            else:
                services = 'No Services'
            record.name = record.date_billed.strftime("%b %Y") + ' | ' + services + ' | ' + record.client_id.name
        return
    
    transaction = fields.Char(string="Transaction id", readonly="1")

    # @api.model
    # def create(self, vals):
    #     name = re.sub(r'\W+', ' ', vals['client_id.name'])
    #     name_array = name.split()
    #     if len(name_array) == 1:
    #         transaction = name_array[0][0:3]
    #     elif len(name_array) == 2:
    #         name1 = name_array[0]
    #         name2 = name_array[1]
    #         transaction = (name1[0:2] if len(name1) >= 2 else name1[0:1]) + \
    #                       (name2[0:2] if len(name1) == 1 else name2[0:1])
    #     elif len(name_array) >= 3:
    #         name1 = name_array[0]
    #         name2 = name_array[1]
    #         name3 = name_array[2]
    #         transaction = name1[0:1] + name2[0:1] + name3[0:1]
    #     # Compute Client ID
    #     transaction += "-" + self.env['ir.sequence'].next_by_code('billing.id.seq')
    #     vals['transaction'] = transaction
    #     return super(BcsBilling, self).create(vals)

    client_id = fields.Many2one(comodel_name='client.profile', string="Client Name", required=True)
    
    @api.onchange('client_id')
    def _onchange_client_id(self):
        
        arj = self.env['soa.ar.journal'].search(
            [('client_id', '=', self.client_id.id)], limit=1)
        if arj:
            self.previous_amount = arj.balance
            
        bs = self.env['billing.summary'].search(
            [('client_id', '=', self.client_id.id)], limit=1)
        if bs:
            self.services_id = bs.service_ids
            self.services_amount = bs.get_services_total_amount(self.services_id)
    
    issued_by = fields.Many2one(comodel_name='hr.employee', string="Issued By")
    # collection_ids = fields.Many2many(comodel_name='bcs.collection', string="Collection")
    # for_collection_updates = fields.Many2many(comodel_name='bcs.updates', string="For-collection Updates") # maybe not needed
    
    date_billed = fields.Date(string="Date Billed")
    state_selection = [('draft', 'Draft'),
                       ('submitted', 'Submitted'),
                       ('verified', 'Verified'),
                       ('approved', 'Approved')]
    state = fields.Selection(state_selection, default='draft', copy=False)

    # ops manager create
    def draft_action(self):
        self.state = 'draft'

    # ops manager
    def ops_manager_submitted_action(self):
        self.state = 'submitted'

    # fad supervisor
    def fad_supervisor_verified_action(self):
        self.state = 'verified'

    # fad manager
    def fsd_manager_approved_action(self):
        self.state = 'approved'
        
        # add to ar journal
        arj = self.env['soa.ar.journal'].search([
            ('client_id', '=', self.client_id.id) ])
        if arj:
            arj = arj[0]
            arj.new_billing(self)
        

    status_selection = [('not_sent', 'Not yet sent'),
                        ('sent_to_client', 'Sent to client'),
                        ('client_received', 'Client has received'),
                        ('void_transaction', 'Void Transaction')]
    status = fields.Selection(status_selection, default='not_sent')
    
    # only appear when status == 'sent_to_client'
    sent_with_email = fields.Boolean(default=True, string="Sent with Email")
    sent_with_errand = fields.Boolean(string="Sent with Errand")
    
    # fad has sent billing to client
    def sent_to_client(self):
        self.status = 'sent_to_client'
        
        # add to for-updates collection
        self.env['bcs.updates'].create({'billing_id': self.id})

    # client confirms they received it
    def client_received(self):
        self.status = 'client_received'
        
    # billing is apparently void
    def void_transaction(self):
        self.status = 'void_transaction'
        
        # update ar journal as well
        arj = self.env['soa.ar.journal'].search([('client_id', '=', self.client_id.id)], limit=1)
        if arj:
            arj.void_transaction(self)

    # @api.constrains('state')
    # def _check_state_for_editing(self):
    #     for record in self:
    #         if record.state == 'approved' and any(
    #                 record[field] != record._origin[field] for field in ['status', 'billing_sent']):
    #             raise ValidationError("Fields can only be edited when state is not 'approved'.")

    other = fields.Text(string="Other Instruction")
    services_id = fields.Many2many(comodel_name="services.type", string="Services", required=True)
    
    @api.onchange('services_id')
    def _onchange_services_id(self):
        bs = self.env['billing.summary'].search(
            [('client_id', '=', self.client_id.id)], limit=1)
        if bs:
            self.services_amount = bs.get_services_total_amount(self.services_id)
    
    previous_amount = fields.Float(string="Previous Amount")
    services_amount = fields.Float(string="Services Amount")
    amount = fields.Float(string="Total Amount", compute="_compute_amount")
    remarks = fields.Text(string="Remarks")
    
    @api.depends('previous_amount', 'services_amount')
    def _compute_amount(self):
        for rec in self:
            rec.amount = rec.previous_amount + rec.services_amount