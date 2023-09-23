from odoo import models, fields, api
import re
from odoo.exceptions import ValidationError
from datetime import datetime


class ClientProfile(models.Model):
    _name = 'client.profile'
    _description = "Profile"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Client Name", required=True)

    @api.onchange('name')
    def caps_name(self):
        if self.name:
            self.name = str(self.name).title()

    is_company = fields.Selection([('individual', 'Individual'), ('company', 'Company')], default="company")
    image_101 = fields.Image(string="Image")
    organization_type = fields.Selection(
        [('sole_proprietor', 'Sole Proprietor'), ('general_partnership', 'General Partnership'),
         ('general_professional', 'General Professional Partnership'),
         ('domestic_stock', 'Domestic Stock Corporation'), ('domestic_nsnp', 'Domestic NSNP Corporation'),
         ('foreign_corporation', 'Branch of Foreign Corporation'),
         ('foreign_nsnp', 'Branch of Foreign NSNP Corporation'), ('rohq', 'ROHQ of Foreign Corporation'),
         ('representative_officer', 'Representative Office')], string="Organization Type")
    industry_class = fields.Selection(
        [('agricultural', 'Agricultural Products & Farming Operations'), ('automotive', 'Automotive & Spare Parts'),
         ('', ''), ('utilities', 'Energy, Utilities & Telecommunications'), ('financial_service', 'Financial Services'),
         ('', ''), ('food', 'Food, Beverage & Restaurant Operations'),
         ('organization', 'Foundations & Non-Profit Organizations'),
         ('appliances', 'Furniture, Appliances & IT Equipment'), ('construction', 'Hardware & Construction Supplies'),
         ('health', 'Healthcare & Pharmaceuticals'), ('hospital', 'Hospitality & Leisure'),
         ('industrial', 'Industrial Manufacturing'),
         ('information_technology', 'IT Services & Business Process Outsourcing'),
         ('retail', 'Lifestyle & Retail Brands'), ('entertainment', 'Media & Entertainment'),
         ('nothing', 'n.e.c. (not elsewhere classified)'),
         ('', ''), ('other_service', 'Other Services'), ('print_service', 'Printing Services'),
         ('consultancy', 'Professional & Consultancy Services'), ('transport', 'Public Transport Services'),
         ('real_estate', 'Real Estate Development & Construction'),
         ('stationery', 'Stationery & Paper Products'), ('logistic', 'Warehousing & Logistics')],
        string="Industry Class")
    nature_of_business = fields.Text(string="Nature of Activities, Brands, Product & Services")
    date_of_engagement = fields.Date(string="Date of Engagement", required=True)
    client_system_generated = fields.Char(string="Client ID")
    tax_reporting_compliance = fields.Boolean(string="Tax Reporting & Compliance")
    annual_registration_update = fields.Boolean(string="Annual Registration Update")
    agree_upon_procedure = fields.Boolean(string="Agree-Upon Procedures")
    audit_assurance = fields.Boolean(string="Audit & Assurance")
    tax_advocacy = fields.Boolean(string="Tax Advocacy(Investigation)")
    advisory_consultancy = fields.Boolean(string="Advisory & Consultancy")
    compilation = fields.Boolean(string="Compilation")
    others = fields.Char(string="Others")
    state = fields.Selection([('draft', 'Draft'),
                              ('supervisor', 'Supervisor'),
                              ('manager', 'Manager'),
                              ('approved', 'Approved'),
                              ('cancel', 'Returned')], default='draft', string="Status")
    associate_id = fields.Many2one(string="Associate", comodel_name="associate.profile", required=True)
    manager_id = fields.Many2one(string="Manager", related="associate_id.manager_id", readonly=True)
    supervisor_id = fields.Many2one(string="Supervisor", related="associate_id.supervisor_id", readonly=True)
    cluster_id = fields.Many2one(string="Cluster", related="associate_id.cluster_id", readonly=True)
    lead_partner_id = fields.Many2one(string="Lead Partner", related="associate_id.lead_partner_id", readonly=True)
    state_sequence = fields.Char(compute='_compute_state_sequence', string='Progress Status', store=True)

    # client_fs_ids = fields.One2many(comodel_name='client.fs', inverse_name="client_fs_id", string="FS")
    # is_editable = fields.Boolean(default=False)
    #
    # def toggle_edit_mode(self):
    #     for record in self:
    #         record.is_editable = not record.is_editable

    @api.depends('state')
    def _compute_state_sequence(self):
        for record in self:
            if record.state == 'draft':
                record.state_sequence = '1.Draft'
            elif record.state == 'supervisor':
                record.state_sequence = '2.Supervisor'
            elif record.state == 'manager':
                record.state_sequence = '3.Manager'
            elif record.state == 'approved':
                record.state_sequence = '4.Approved'

            else:
                record.state_sequence = 'Unknown'

    def draft_action(self):
        self.state = 'draft'

    def action_submit_supervisor(self):
        self.state = 'supervisor'
        # return {
        #     'name':'Supervisor',
        #     'view_type':'form',
        #     'view_mode':'tree,form',
        #     'res_model':'client.profile',
        #     'type':'ir.actions.act_window',
        #     'target':'inline',
        #     'flags':{'form':{'action_button':True}},
        # }

    def action_approve_supervisor(self):
        self.state = 'manager'

    def action_return(self):
        self.state = 'cancel'

    def action_approve_manager(self):
        self.state = 'approved'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Approved',
                'type': 'rainbow_man'
            }
        }

    # @api.onchange("name")
    # def compute_name(self):
    #     client_id = ""
    #     if self.date_of_engagement:
    #         name = re.sub(r'\W+', ' ', self.name)
    #         name_array = name.split()
    #         if len(name_array) == 1:
    #             client_id = name_array[0][0:3]
    #         elif len(name_array) == 2:
    #             name1 = name_array[0]
    #             name2 = name_array[1]
    #             print(name1, name2)
    #             client_id = (name1[0:2] if len(name1) >= 2 else name1[0:1]) + \
    #                         (name2[0:2] if len(name1) == 1 else name2[0:1])
    #         elif len(name_array) >= 3:
    #             name1 = name_array[0]
    #             name2 = name_array[1]
    #             name3 = name_array[2]
    #             client_id = name1[0:1] + name2[0:1] + name3[0:1]
    #
    #         print(client_id.upper())
    def write(self, vals):
        if 'name' in vals:
            old_id = self.client_system_generated.split("-")[0]
            name = re.sub(r'\W+', ' ', vals['name'])
            name_array = name.split()

            if len(name_array) == 1:
                client_system_generated = name_array[0][0:3]
            elif len(name_array) == 2:
                name1 = name_array[0]
                name2 = name_array[1]
                client_system_generated = (name1[0:2] if len(name1) >= 2 else name1[0:1]) + \
                                          (name2[0:2] if len(name1) == 1 else name2[0:1])
            elif len(name_array) >= 3:
                name1 = name_array[0]
                name2 = name_array[1]
                name3 = name_array[2]
                client_system_generated = name1[0:1] + name2[0:1] + name3[0:1]
            vals.update({'client_system_generated': self.client_system_generated.replace(old_id,
                                                                                         client_system_generated).upper()})
        super(ClientProfile, self).write(vals)

    @api.model
    def create(self, vals):
        name = re.sub(r'\W+', ' ', vals['name'])
        name_array = name.split()
        if len(name_array) == 1:
            client_system_generated = name_array[0][0:3]
        elif len(name_array) == 2:
            name1 = name_array[0]
            name2 = name_array[1]
            client_system_generated = (name1[0:2] if len(name1) >= 2 else name1[0:1]) + \
                                      (name2[0:2] if len(name1) == 1 else name2[0:1])
        elif len(name_array) >= 3:
            name1 = name_array[0]
            name2 = name_array[1]
            name3 = name_array[2]
            client_system_generated = name1[0:1] + name2[0:1] + name3[0:1]
        # Compute Client ID
        client_system_generated += "-" + ("0" if int(
            datetime.strftime(datetime.strptime(vals['date_of_engagement'], '%Y-%m-%d'), '%Y')) < 2000 else "1") + \
                                   str(vals['date_of_engagement'])[2:4] + \
                                   str(vals['date_of_engagement'])[5:7] + "-" + \
                                   self.env['ir.sequence'].next_by_code('client.id.seq')

        vals.update({'client_system_generated': client_system_generated.upper()})
        res = super(ClientProfile, self).create(vals)
        if res:
            self.env['escalation.contact'].create({
                'level': 'level_1',
                'timeframe': 'lvl1',
                'escalation_id': res.id
            })
            self.env['escalation.contact'].create({
                'level': 'level_2',
                'timeframe': 'lvl2',
                'escalation_id': res.id
            })
            self.env['escalation.contact'].create({
                'level': 'level_3',
                'timeframe': 'lvl3',
                'escalation_id': res.id
            })
        return res

    unit_no = fields.Char(string="Unit/Floor")
    building_name = fields.Char(string="Building Name")
    street = fields.Char(string="Street")
    district = fields.Char(string="District/Barangay/Village")
    city = fields.Char(string="City")
    zip = fields.Char(string="Zip Code", size=4)

    @api.constrains('zip')
    def _validate_zip(self):
        for record in self:
            pattern = r'^\d{4}$'  # Modify the regular expression pattern according to your requirements
            if record.zip and not re.match(pattern, record.zip):
                raise ValidationError('Invalid Zip Code!')

    landline = fields.Char(string="Telephone", help="This field includes a hyphen", size=13)

    @api.constrains('landline')
    def _validate_landline(self):
        for record in self:
            pattern = r'^\d{4}-\d{4}-\d{3}$'
            if record.landline and not re.match(pattern, record.landline):
                raise ValidationError('Invalid telephone number format ex:0000-0000-local number!')

    facsimile_no = fields.Char(string="Facsimile", help="This field includes a hyphen", size=13)

    @api.constrains('facsimile_no')
    def _validate_facsimile_no(self):
        for record in self:
            pattern = r'^\d{4}-\d{4}-\d{3}$'
            if record.facsimile_no and not re.match(pattern, record.facsimile_no):
                raise ValidationError('Invalid telephone number format ex:0000-0000-local number!')

    website = fields.Char(string="Website")
    unit_no2 = fields.Char(string="Unit/Floor")
    building_name2 = fields.Char(string="Building Name")
    street2 = fields.Char(string="Street")
    district2 = fields.Char(string="District/Barangay/Village")
    city2 = fields.Char(string="City")
    zip2 = fields.Char(string="Zip Code", size=4)

    @api.constrains('zip2')
    def _validate_zip2(self):
        for record in self:
            pattern = r'^\d{4}$'  # Modify the regular expression pattern according to your requirements
            if record.zip2 and not re.match(pattern, record.zip2):
                raise ValidationError('Invalid Zip Code!')

    landline2 = fields.Char(string="Telephone", help="This field includes a hyphen", size=13)

    @api.constrains('landline2')
    def _validate_landline2(self):
        for record in self:
            pattern = r'^\d{4}-\d{4}-\d{3}$'
            if record.landline2 and not re.match(pattern, record.landline2):
                raise ValidationError('Invalid telephone number format ex:0000-0000-local number!')

    primary_contact_person = fields.Char(string="Primary Contact")
    mobile_number = fields.Char(string="Mobile No.")

    @api.constrains('mobile_number')
    def _validate_mobile_number(self):
        for record in self:
            pattern = r'^(?:\+63|0)\d{10}$'  # Modify the regular expression pattern according to your requirements
            if record.mobile_number and not re.match(pattern, record.mobile_number):
                raise ValidationError('Invalid mobile number format!')

    email_address = fields.Char(string="Email Address")
    principal_accounting_officer = fields.Char(string="Principal Accounting Officer")
    landline3 = fields.Char(string="Telephone", help="This field includes a hyphen", size=13)

    @api.constrains('landline3')
    def _validate_landline3(self):
        for record in self:
            pattern = r'^\d{4}-\d{4}-\d{3}$'
            if record.landline3 and not re.match(pattern, record.landline3):
                raise ValidationError('Invalid telephone number format ex:0000-0000-local number!')

    mobile_number2 = fields.Char(string="Mobile No.")

    @api.constrains('mobile_number2')
    def _validate_mobile_number2(self):
        for record in self:
            pattern = r'^(?:\+63|0)\d{10}$'  # Modify the regular expression pattern according to your requirements
            if record.mobile_number2 and not re.match(pattern, record.mobile_number2):
                raise ValidationError('Invalid mobile number format!')

    email_address2 = fields.Char(string="Email Address")
    corporate_ids = fields.One2many(comodel_name='corporate.officer', inverse_name='client_profile_ids',
                                    string="Corporate Officers")
    vat = fields.Char(string="Tax ID No.", size=11)

    @api.onchange('vat')
    def onchange_vat(self):
        if self.vat and len(self.vat) == 9:
            formatted_value = '-'.join([self.vat[:3], self.vat[3:6], self.vat[6:]])
            self.vat = formatted_value

    @api.constrains('vat')
    def _check_vat(self):
        for record in self:
            if record.vat:
                if any(char.isalpha() and char != '-' for char in record.vat):
                    raise ValidationError(
                        "Only numbers are allowed in the TAX ID Number.")

    rdo_code = fields.Char(string="RDO Code", size=4)

    @api.constrains('rdo_code')
    def _validate_rdo_code(self):
        for record in self:
            pattern = r'^\d{4}$'  # Modify the regular expression pattern according to your requirements
            if record.rdo_code and not re.match(pattern, record.rdo_code):
                raise ValidationError('Invalid RDO Code!')

    registration_date = fields.Date('Date')
    income_tax = fields.Boolean(string="Income Tax")
    excise_tax = fields.Boolean(string="Excise Tax")
    value_added_tax = fields.Boolean(string="Value-added Tax")
    withholding_tax_expanded = fields.Boolean(string="Withholding Tax - Expanded")
    withholding_tax_compensation = fields.Boolean(string="Withholding Tax - Compensation")
    withholding_tax_final = fields.Boolean(string="Withholding Tax - Final")
    registration_fee = fields.Boolean(string="Registration Fee")
    other_percentage_tax = fields.Boolean(string="Other Percentage Tax")
    other_percentage_tax1 = fields.Char()
    tax_type = fields.Selection([
        ('regular', 'Regular'), ('top_5k_individual', 'Top 5k Individual'), (
            'top_20k_corporate', 'Top 20k Corporate'), ('medium_taxpayer', 'Medium Taxpayer'), (
            'large_taxpayer', 'Large Taxpayer')], string="Taxpayer Type")
    invoice_tax = fields.Selection([
        ('bound_padded', 'Bound (Padded)'), ('computer_aid_loose_leaf', 'Computer-aided (Loose-leaf)'), (
            'cas_generated', 'CAS-Generated')], string="Invoice Type")
    filing_payment = fields.Selection([('ebir_manual', 'eBIR (Manual)'), ('efps', 'EFPS')], string="Filling & Payment")
    books_of_account = fields.Selection(
        [('manual', 'Manual'), ('computer_aid_loose_leaf', 'Computer-aided (Loose-leaf)'),
         ('cas_generated', 'CAS-Generated')], string="Books of Accounts")
    psic_psoc = fields.Char(string="PSIC/PSOC")
    ll_cas_permit_no = fields.Char(string="LL/CAS Permit No")
    ask = fields.Selection([('yes', 'Yes'), ('no', 'No')], default="no")
    registration_number = fields.Char(string="Registration No", size=13)

    @api.onchange('registration_number')
    def set_upper(self):
        self.registration_number = str(self.registration_number).upper()
        return

    registration_date_sec = fields.Date('Date')
    trade_name = fields.Char(string="Trade Name")
    date_per_law = fields.Char(string="Date per By-Laws")
    actual_date_meeting = fields.Date('date')
    ask_1 = fields.Selection([('yes', 'Yes'), ('no', 'No')], default="no")
    ask_2 = fields.Text(string="If Yes what type of security is the Company permit to sell?")
    class_shares_id = fields.One2many(comodel_name='class.of.shares', inverse_name='client_share_ids',
                                      string="Class of Shares")
    ask_3 = fields.Selection([('yes', 'Yes'), ('no', 'No')], default="no")
    bureau_of_custom = fields.Boolean(string="Bureau of Customs")
    attachment = fields.Many2many('ir.attachment', 'attachment_rel', 'pro_id', 'attach_id', string='Attachments', )
    attachment_fname = fields.Char(string="Attachment Filename")
    bangko_sentral_pilipinas = fields.Boolean(string="Bangko Sentral ng Pilipinas")
    professional_regulation_commission = fields.Boolean(string="Professional Regulation Commission")
    philippines_council_ngo_certification = fields.Boolean(string="Philippine Council for NGO Certification")
    cooperative_development_authority = fields.Boolean(string="Cooperative Development Authority")
    insurance_commission = fields.Boolean(string="Insurance Commission")
    integrated_bar_philippines = fields.Boolean(string="Integrated Bar of the Philippines")
    philippines_stock_exchange = fields.Boolean(string="Philippine Stock Exchange")
    construction_industry_authority_philippines = fields.Boolean(
        string="Construction Industry authority of the Philippines (PCAB)")
    philippine_amusement_gaming_corporation = fields.Boolean(string="Philippine Amusement and Gaming Corporation")
    land_transportation_franchising_regulatory_board = fields.Boolean(
        string="Land Transportation Franchising and Regulatory Board")
    others_ri = fields.Boolean(string="Others")
    others_reg = fields.Char(string="Others")
    sss = fields.Char(string="SSS ER No", size=15)

    @api.onchange('sss')
    def onchange_sss(self):
        for record in self:
            if record.sss and len(record.sss) == 13:
                formatted_number = '-'.join([
                    record.sss[:2],
                    record.sss[2:10],
                    record.sss[10:]
                ])
                record.sss = formatted_number

    @api.constrains('sss')
    def _check_sss(self):
        for record in self:
            if record.sss:
                if any(char.isalpha() and char != '-' for char in record.sss):
                    raise ValidationError(
                        "Only numbers are allowed in the SSS Number.")

    phic = fields.Char(string="PHIC ER No", size=14)

    @api.onchange('phic')
    def onchange_phic(self):
        for record in self:
            if record.phic and len(record.phic) == 12:
                formatted_number = '-'.join([
                    record.phic[:2],
                    record.phic[2:11],
                    record.phic[11:]
                ])
                record.phic = formatted_number

    @api.constrains('phic')
    def _check_phic(self):
        for record in self:
            if record.phic:
                if any(char.isalpha() and char != '-' for char in record.phic):
                    raise ValidationError(
                        "Only numbers are allowed in the PHIC Number.")

    hdmf = fields.Char(string="HDMF ER No", size=14)

    @api.onchange('hdmf')
    def onchange_hdmf(self):
        for record in self:
            if record.hdmf and len(record.hdmf) == 12:
                formatted_number = '-'.join([
                    record.hdmf[:4],
                    record.hdmf[4:8],
                    record.hdmf[8:]
                ])
                record.hdmf = formatted_number

    @api.constrains('hdmf')
    def _check_hdmf(self):
        for record in self:
            if record.hdmf:
                if any(char.isalpha() and char != '-' for char in record.hdmf):
                    raise ValidationError(
                        "Only numbers are allowed in the HDMF Number.")

    sss_filing = fields.Selection([('manual', 'Manual'), ('online', 'Online (AMS-CCL)')], string="Filing")
    phic_filing = fields.Selection([('manual', 'Manual'), ('online', 'Online (ERPS)')], string="Filing")
    hdmf_filing = fields.Selection([('manual', 'Manual'), ('online', 'Online (eSRS)')], string="Filing")
    sss_pay = fields.Selection([('cash', 'Cash'), ('check', 'Check'), ('online_banking', 'Online Banking (EPS)')],
                               string="Payment")
    phic_pay = fields.Selection([('cash', 'Cash'), ('check', 'Check'), ('online_banking', 'Online Banking (EPS)')],
                                string="Payment")
    hdmf_pay = fields.Selection([('cash', 'Cash'), ('check', 'Check'), ('online_banking', 'Online Banking (EPS)')],
                                string="Payment")
    escalation = fields.One2many(comodel_name='escalation.contact', inverse_name='escalation_id',
                                 string="Escalation Point")
    # # client_records
    # documents_count = fields.Integer(compute="action_attach_documents")
    #
    # def action_attach_documents(self):
    #     for rec in self:
    #         rec.documents_count = self.env['client.records'].search_count([
    #             ('client_profile_id', '=', rec.id)
    #         ])
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Working Papers',
    #         'res_model': 'client.records',
    #         'view_mode': 'kanban,form',
    #         'domain': [('client_profile_id', '=', rec.id)],
    #         'context': {'default_client_profile_id': rec.id},
    #         'target': 'current',
    #     }

    # # working papers
    # upload_file = fields.Binary(string='File', attachment=True)
    # file_name = fields.Char(string='Filename')
    # year_field = fields.Date(string="Year")
