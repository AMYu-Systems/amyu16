from odoo import fields, models, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)
def test_with_logger(data: any = "Debug Message", warn: bool = False):
    """Outputs a debug message in the odoo log file, 5 times in a row"""
    method = _logger.info if not warn else _logger.warning
    for _ in range(5):
        method(data)



class BcsBilling(models.Model):
    _name = 'bcs.billing'
    _description = "Billing"
    _rec_name = 'name'
    # _rec_name = 'transaction'

    name = fields.Char(compute="_compute_name")
    transaction = fields.Char(string="Billing Invoice No.", readonly="1")
    client_id = fields.Many2one(comodel_name='client.profile', string="Client Name", required=True, tracking=True)
    ar_journal_id = fields.Many2one(comodel_name='soa.ar.journal', string="AR Journal", compute='_compute_arj', store=True)
    billing_summary_id = fields.Many2one(comodel_name='billing.summary', compute='_compute_billing_summary', store=True)
    
    
    @api.depends("service_ids", "date_billed", "client_id.name")
    def _compute_name(self):
        for record in self:
            services = BcsBilling.get_services_str(record)
            record.name = str(record.transaction) + ' | ' + record.date_billed.strftime("%b %Y") \
                          + ' | ' + services + ' | ' + record.client_id.name
        return
    
    
    @api.depends('client_id')
    def _compute_arj(self):
        for record in self:
            arj = self.env['soa.ar.journal'].search([('client_id', '=', record.client_id.id)], limit=1)
            if arj:
                record.ar_journal_id = arj
        return
    
    
    @api.depends('client_id')
    def _compute_billing_summary(self):
        for record in self:
            bs = self.env['billing.summary'].search([('client_id', '=', record.client_id.id)], limit=1)
            if bs:
                record.billing_summary_id = bs
        return
    
    
    @staticmethod
    def get_services_str(record) -> str:
        services = ''
        separator = ', '
        if len(record.service_ids) > 0:
            for service in record.service_ids:
                services += service.code + separator
            services = services[:-2]
        else:
            services = 'No Services'
        return services
    
    
    @api.model
    def create(self, vals):
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

        # Compute Client ID
        # transaction += "-" + self.env['ir.sequence'].next_by_code('billing.id.seq')
        res = super(BcsBilling, self).create(vals)
        if res:
            res.transaction = f'{res.id:05d}'
            prev_billing = self.env['bcs.billing'].search(
                [('client_id', '=', res.client_id.id), ('state', '=', 'approved'), 
                 ('status', '=', 'void_billing')], 
                order='id desc', limit=1)
            if prev_billing:
                res.previous_voided_billing = prev_billing
                prev_billing.next_approved_after_void = res
        return res


    @api.onchange('client_id')
    def _onchange_client_id(self):
        if self.client_id:
            arj = self.ar_journal_id
            if arj and arj.balance:
                self.previous_amount = arj.balance
            elif not arj:
                raise ValidationError('No AR Journal found for this Client.')

            bs = self.billing_summary_id
            if bs:
                # raise ValidationError(bs.service_ids)
                self.allowed_service_ids = [(6, 0, [srv.id for srv in bs.service_ids])]
                self.service_ids = [(6, 0, [srv.id for srv in bs.service_ids])]
                self._set_billing_services()
            else:
                raise ValidationError('No Billing Summary found for this Client.')


    @api.model
    def _default_issued_by(self):
        if not self.env.user or not self.env.user.id:
            return False
        return self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)
        
        
    issued_by = fields.Many2one(comodel_name='hr.employee', string="Issued By", default=_default_issued_by, tracking=True)
    date_billed = fields.Date(string="Date Billed", required=True, default=fields.Date.today, tracking=True)
    state_selection = [('draft', 'Draft'),
                       ('submitted', 'Submitted'),
                       ('verified', 'Verified'),
                       ('approved', 'Approved')]
    state = fields.Selection(state_selection, default='draft', copy=False, store=True, tracking=True)


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
        if self.ar_journal_id:
            self.ar_journal_id.new_billing(self)
            # check if billing amount is less than ar balance
            if self.amount <= 0:
                # MATIC WALANG BAYAD
                update = self.env['bcs.updates'].create({
                    'billing_id': self.id,
                    'confirmed_remarks': '[System Remarks: Remaining Balance is more than Billing amount]',
                })
                if update:
                    update.set_confirmed_payment()


    allow_void = fields.Boolean(default=True)
    previous_voided_billing = fields.Many2one(comodel_name='bcs.billing', ref='previous_voided_billing')
    next_approved_after_void = fields.Many2one(comodel_name='bcs.billing', ref='next_approved_after_void', 
                                               string='Next Approved Billing')
    void_reason = fields.Text(string="Reason for Void")
    void_attachment = fields.Many2many('ir.attachment', string="Attachment for Void")
    
    status_selection = [('not_sent', 'Not yet sent'),
                        ('sent_to_client', 'Sent to client'),
                        ('client_received', 'Client has received'),
                        ('client_paid', 'Client has paid'),
                        ('void_billing', 'Void Statement')]
    status = fields.Selection(status_selection, default='not_sent', store=True, tracking=True)

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


    # client has paid the billing
    def client_paid(self):
        # '''
        # This function is only called by bcs_collection.py.
        # Even if not complete, as long as collection exists, the client has "paid" the billing.
        # This is the basis of the Collection Report (?)
        # '''
        self.status = 'client_paid'


    # billing is apparently void
    def void_billing(self):
        if not self.allow_void:
            return

        self.status = 'void_billing'

        # CONSTRAINT: check first if the most recent billing, is the same as this record
        # past billings can no longer be voided
        most_recent_billing = self.env['bcs.billing'].search(
            [('state', '=', 'approved'), ('client_id', '=', self.client_id.id)],
            order="transaction desc", limit=1)
        if most_recent_billing.id != self.id:
            self.allow_void = False
            return

        # update ar journal
        if self.ar_journal_id:
            self.ar_journal_id.void_billing(self)


    def set_allow_void_false(self):
        ''' Triggered by Collection class '''
        self.allow_void = False

    # @api.constrains('state')
    # def _check_state_for_editing(self):
    #     for record in self:
    #         if record.state == 'approved' and any(
    #                 record[field] != record._origin[field] for field in ['status', 'billing_sent']):
    #             raise ValidationError("Fields can only be edited when state is not 'approved'.")

    # other = fields.Text(string="Other Instruction", tracking=True)
    service_ids = fields.Many2many(comodel_name="services.type", string="Services", required=True, 
                                   relation="bcs_billing_selected_services_rel", track_visibility=True)
    allowed_service_ids = fields.Many2many(comodel_name="services.type", string="Allowed Services",
                                           relation="bcs_billing_allowed_services_rel")
    # for all services as one general record
    billing_service_ids = fields.Many2many(comodel_name='billing.service', store=True)
    
    
    def _set_billing_services(self):
        included_services = self.env['services.type'].search([('code','in', [s.code for s in self.service_ids])])
        bserv_int_ids = self.billing_summary_id.get_service_records_as_int_list(included_services)
        self.billing_service_ids = [(6, 0, bserv_int_ids)]
    
    
    @api.onchange('service_ids')
    def _onchange_service_ids(self):
        '''
        Need for displaying amounts for Billing Summary of client in Billing
        '''
        bs = self.billing_summary_id
        if bs:
            # self.services_amount = bs.get_services_total_amount(self.service_ids) # Total amount only
            # Get all billing service ids approach
            self._set_billing_services()
            
    
    @api.onchange('billing_service_ids')
    def _onchange_billing_service_ids(self):
        total = 0
        for bserv in self.billing_service_ids:
            total += bserv.amount
        self.services_amount = total
     
            
    active_billing = fields.Boolean(string="Active Billing", compute="_compute_active_billing", store=True)
    previous_amount = fields.Float(string="Previous Amount", tracking=0)
    services_amount = fields.Float(string="Services Amount", tracking=0)
    
    has_adjustments = fields.Boolean(default=False)
    adjustment_ids = fields.One2many(comodel_name='bcs.billing.adjustment', 
                                     inverse_name='billing_id', string='Adjustments')
    adjustments_amount = fields.Float(compute='_compute_adjustments_amount')
    
    amount = fields.Float(string="Total Amount", compute="_compute_amount")
    remarks = fields.Text(string="Remarks", tracking=0)
    
    
    def add_adjustments(self):
        ''' Button trigger from XML '''
        self.has_adjustments = True
    
        
    def remove_adjustments(self):
        ''' Button trigger from XML '''
        self.has_adjustments = False
        self.adjustment_ids = [(6, 0, [])] # delete all adjustments
    
    
    @api.depends('adjustment_ids')
    def _compute_adjustments_amount(self):
        '''
        Compute the total amount of adjustments added (`adjustment_ids`)
        '''
        for record in self:
            total = 0
            for adj_id in record.adjustment_ids:
                total += adj_id.amount
            record.adjustments_amount = total
    
    
    @api.depends('previous_amount', 'services_amount', 'has_adjustments', 'adjustments_amount')
    def _compute_amount(self):
        '''
        Depends on: `'previous_amount', 'services_amount', 'has_adjustments', 'adjustments_amount'`
        '''
        for record in self:
            amount = record.previous_amount + record.services_amount
            if record.has_adjustments:
                amount += record.adjustments_amount
            record.amount = amount


    @api.depends('amount', 'state', 'status', 'ar_journal_id.balance', 'ar_journal_id.most_recent_billing_id')
    def _compute_active_billing(self):
        '''
        For each record: \n
        if amount is less than 0, its already paid -> not active anymore \n
        if billing is void, then disregard -> not active anymore \n
        if its not the most recent billing of the client -> not active anymore \n
        if its recent billing but balance is already paid -> not active anymore
        '''
        for record in self:
            arj = record.ar_journal_id
            mrb_id = arj.most_recent_billing_id
            # test_with_logger(str(arj.balance))
            # test_with_logger(str(mrb_id.id), str(record.id),)
            
            if record.amount <= 0 \
            or record.state != 'approved' \
            or record.status == 'void_billing' \
            or mrb_id.id != record.id \
            or (mrb_id.id == record.id and arj.balance <= 0):
                record.active_billing = False
            else:
                record.active_billing = True
    
    # def new_adjustment(self):
        # adj_id = self.env['bcs.billing.adjustment'].create({})
        # adjustment_ids = [] # add
    

class BcsBillingAdjustment(models.Model):
    _name = 'bcs.billing.adjustment'
    _description = "Billing Adjustment"
    # _rec_name = 'name'
    
    details = fields.Text()
    amount = fields.Float()
    
    billing_id = fields.Many2one(comodel_name='bcs.billing')
