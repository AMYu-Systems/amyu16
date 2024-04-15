from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)

# Test
def test_with_logger(data: any="Debug Message", warn: bool = False) -> None:
    """
        Outputs a debug message in the odoo log file, 5 times in a row
    """
    method = _logger.info if not warn else _logger.warning
    for _ in range(5):
        method(data)

class BillingSummary(models.Model):
    _name = 'billing.summary'
    _description = "Billing Summary"
    _rec_name = 'client_id'
    _sql_constraints = [
        (
            'unique_client_id', 
            'unique(client_id)',
            'Can\'t have duplicate clients.'
        )
    ]
    
    client_id = fields.Many2one(string="Client Name", comodel_name='client.profile', required=True)
    
    image_1012 = fields.Image(string="Image")
    partner_id = fields.Many2one(related='client_id.lead_partner_id', string="Partner")
    manager_id = fields.Many2one(related='client_id.manager_id', string="Manager")
    supervisor_id = fields.Many2one(related='client_id.supervisor_id', string="Supervisor")
    associate_id = fields.Many2one(related='client_id.user_id', string="Associate")
    service_ids = fields.Many2many(comodel_name='services.type', string="Type of Services")
    audit_ids = fields.One2many(comodel_name='audit.billing', inverse_name='billing_summary_id', string="Audit")
    trc_ids = fields.One2many(comodel_name='trc.billing', inverse_name='billing_summary_id', string="TRC")
    books_ids = fields.One2many(comodel_name='books.billing', inverse_name='billing_summary_id', string="Books")
    permit_ids = fields.One2many(comodel_name='business.permit.billing', inverse_name='billing_summary_id',
                                 string="Business Permit")
    gis_ids = fields.One2many(comodel_name='gis.billing', inverse_name='billing_summary_id', string="GIS")
    loa_ids = fields.One2many(comodel_name='loa.billing', inverse_name='billing_summary_id', string="LOA")
    spe_ids = fields.One2many(comodel_name='special.engagement', inverse_name='billing_summary_id',
                              string="Special Engagement")
    
    has_aud = fields.Boolean(default=False)
    has_trc = fields.Boolean(default=False)
    has_bks = fields.Boolean(default=False)
    has_per = fields.Boolean(default=False)
    has_gis = fields.Boolean(default=False)
    has_loa = fields.Boolean(default=False)
    has_spe = fields.Boolean(default=False)
    
    # state_selection = [('draft', 'Draft'),
    #                    ('submitted', 'Submitted'),
    #                    ('verified', 'Verified'),
    #                    ('approved', 'Approved')]
    # state = fields.Selection(state_selection, default='draft', copy=False)

    # # auto create or when "edit -> draft" has been implemented
    # def draft_action(self):
    #     self.state = 'draft'

    # # ops manager press submit
    # def submitted_action(self):
    #     self.state = 'submitted'

    # # fad supervisor press verify
    # def verified_action(self):
    #     self.state = 'verified'

    # # fad manager press approve
    # def approved_action(self):
    #     self.state = 'approved'

    def get_services(self):
        services = self.env['billing.summary'].search([('service_ids', '!=', False)])
        return services
    
    def create_billing_service_records(self):
        pass
    
    @api.model
    def create(self, vals):
        res = super(BillingService, self).create(vals)
        
        billing_service_ids = []
        billing_service_ids.append(self.env['bcs.billing.service'].create({
            'service_view': service_tuple[0],
            'amount': service_tuple[1],
        }))

    @api.onchange('service_ids')
    def _onchange_services(self):
        service_list = []
        for service in self.service_ids:
            service_list.append(service.code)
        self.has_aud = 'AUD' in service_list
        self.has_trc = 'TRC' in service_list
        self.has_bks = 'BKS' in service_list
        self.has_per = 'PER' in service_list
        self.has_gis = 'GIS' in service_list
        self.has_loa = 'LOA' in service_list
        self.has_spe = 'SPE' in service_list
        return
    
    def get_services_total_amount(self, included_services_id):
        included = []
        total = 0
        
        included_code = []
        for service_id in included_services_id:
            included_code.append(service_id.code)
        
        if 'AUD' in included_code and self.has_aud: included.append(self.audit_ids)
        if 'TRC' in included_code and self.has_trc: included.append(self.trc_ids)
        if 'BKS' in included_code and self.has_bks: included.append(self.books_ids)
        if 'PER' in included_code and self.has_per: included.append(self.permit_ids)
        if 'GIS' in included_code and self.has_gis: included.append(self.gis_ids)
        if 'LOA' in included_code and self.has_loa: included.append(self.loa_ids)
        if 'SPE' in included_code and self.has_spe: included.append(self.spe_ids)
            
        for services in included: 
            for rec in services:
                total += rec.amount
        return total
    
    def get_services_each_amount(self, included_services_id):
        
        service_amount = []
        def _set_service_amount(service_type, service_ids):
            view = service_type.name + f' ({service_type.code})'
            for service in service_ids:
                service_amount.append((view, service.amount))
        
        included = {}
        for service_id in included_services_id:
            included[service_id.code] = service_id
        
        if 'AUD' in included.keys() and self.has_aud: 
            _set_service_amount(included['AUD'], self.audit_ids)
        if 'TRC' in included.keys() and self.has_trc: 
            _set_service_amount(included['TRC'], self.trc_ids)
        if 'BKS' in included.keys() and self.has_bks: 
            _set_service_amount(included['BKS'], self.books_ids)
        if 'PER' in included.keys() and self.has_per: 
            _set_service_amount(included['PER'], self.permit_ids)
        if 'GIS' in included.keys() and self.has_gis: 
            _set_service_amount(included['GIS'], self.gis_ids)
        if 'LOA' in included.keys() and self.has_loa: 
            _set_service_amount(included['LOA'], self.loa_ids)
        if 'SPE' in included.keys() and self.has_spe: 
            _set_service_amount(included['SPE'], self.spe_ids) 
        
        return service_amount
    

class BillingService(models.Model):
    _name = 'billing.service'
    _description = "Billing Services"
    _rec_name = 'name'
    
    billing_summary_id = fields.Many2one('billing.summary', readonly=True, ondelete='cascade')
    service_view = fields.Char(required=True, readonly=True)
    amount = fields.Float(required=True, readonly=True)
    name = fields.Char(readonly=True, compute='_compute_name')
    
    @api.depends('service_view', 'amount')
    def _compute_name(self):
        for record in self:
            record.name = f'{record.service_view} - PHP {record.amount}'