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

    image_101 = fields.Image(string="Image")
    organization_type = fields.Selection(
        [('sole_proprietor', 'Sole Proprietor'),
         ('general_partnership', 'General Partnership'),
         ('general_professional_partnership', 'General Professional Partnership'),
         ('domestic_stock', 'Domestic Stock Corporation'),
         ('domestic_corp', 'Domestic NSNP Corporation'),
         ('foreign_corp', 'Branch of Foreign Corporation'),
         ('foreign_nsnp_corp', 'Branch of Foreign NSNP Corporation'),
         ('roqh_foreign_corp', 'ROHQ of Foreign Corporation'),
         ('representative_office', 'Representative Office')], string="Organization Type", required=True)
    sole_proprietor_ids = fields.One2many(comodel_name='sole.proprietor', inverse_name='sole_proprietor_id',
                                          string="Sole")
    general_partnership_ids = fields.One2many(comodel_name='general.partnership', inverse_name='general_partnership_id',
                                              string="General")
    general_professional_partnership_ids = fields.One2many(comodel_name='general.professional.partnership',
                                                           inverse_name='general_professional_partnership_id',
                                                           string="General Professional")
    domestic_stock_ids = fields.One2many(comodel_name='domestic.stock', inverse_name='domestic_stock_id',
                                         string="Domestic")
    domestic_corp_ids = fields.One2many(comodel_name='domestic.corp', inverse_name='domestic_corp_id',
                                        string="Domestic NSNP")
    foreign_corp_ids = fields.One2many(comodel_name='foreign.corp', inverse_name='foreign_corp_id',
                                       string="Foreign Corp")
    foreign_nsnp_corp_ids = fields.One2many(comodel_name='foreign.nsnp.corp', inverse_name='foreign_nsnp_corp_id',
                                            string="Foreign NSNP Corp")
    roqh_foreign_corp_ids = fields.One2many(comodel_name='roqh.foreign.corp', inverse_name='roqh_foreign_corp_id',
                                            string="ROQH Foreign Corp")
    representative_office_ids = fields.One2many(comodel_name='representative.office',
                                                inverse_name='representative_office_id',
                                                string="Representative Office")
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

    @api.onchange('nature_of_business')
    def caps_nature_of_business(self):
        if self.nature_of_business:
            self.nature_of_business = str(self.nature_of_business).title()

    @api.onchange('nature_of_business')
    def _onchange_nature_of_business(self):
        for record in self:
            if any(char.isdigit() for char in record.nature_of_business):
                raise ValidationError("Numbers are not allowed in this Field.")

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

    @api.onchange('unit_no')
    def caps_unit_no(self):
        if self.unit_no:
            self.unit_no = str(self.unit_no).title()

    building_name = fields.Char(string="Building Name")

    @api.onchange('building_name')
    def caps_building_name(self):
        if self.building_name:
            self.building_name = str(self.building_name).title()

    street = fields.Char(string="Street")

    @api.onchange('street')
    def caps_street(self):
        if self.street:
            self.street = str(self.street).title()

    district = fields.Char(string="District/Barangay/Village")

    @api.onchange('district')
    def caps_district(self):
        if self.district:
            self.district = str(self.district).title()

    city = fields.Char(string="City")

    @api.onchange('city')
    def caps_city(self):
        if self.city:
            self.city = str(self.city).title()

    zip = fields.Char(string="Zip Code", size=4)

    @api.constrains('zip')
    def _validate_zip(self):
        for record in self:
            pattern = r'^\d{4}$'  # Modify the regular expression pattern according to your requirements
            if record.zip and not re.match(pattern, record.zip):
                raise ValidationError('Invalid Zip Code!')

    landline = fields.Char(string="Telephone", size=16)

    @api.onchange('landline')
    def onchange_landline(self):
        for record in self:
            if record.landline and len(record.landline) == 13:
                formatted_number = '-'.join([
                    record.landline[:2],
                    record.landline[2:6],
                    record.landline[6:10],
                    record.landline[10:]
                ])
                record.landline = formatted_number

    @api.constrains('landline')
    def _check_landline(self):
        for record in self:
            if record.landline:
                if any(char.isalpha() and char != '-' for char in record.landline):
                    raise ValidationError(
                        "Only numbers are allowed in the Telephone Number.")

    facsimile_no = fields.Char(string="Facsimile", size=16)

    @api.onchange('facsimile_no')
    def onchange_facsimile_no(self):
        for record in self:
            if record.facsimile_no and len(record.facsimile_no) == 13:
                formatted_number = '-'.join([
                    record.facsimile_no[:2],
                    record.facsimile_no[2:6],
                    record.facsimile_no[6:10],
                    record.facsimile_no[10:]
                ])
                record.facsimile_no = formatted_number

    @api.constrains('facsimile_no')
    def _check_facsimile_no(self):
        for record in self:
            if record.facsimile_no:
                if any(char.isalpha() and char != '-' for char in record.facsimile_no):
                    raise ValidationError(
                        "Only numbers are allowed in the Facsimile Number.")

    website = fields.Char(string="Website")

    @api.onchange('website')
    def _onchange_website(self):
        for record in self:
            if any(char.isdigit() for char in record.website):
                raise ValidationError("Numbers are not allowed in the Website Field.")

    unit_no2 = fields.Char(string="Unit/Floor")

    @api.onchange('unit_no2')
    def caps_unit_no2(self):
        if self.unit_no2:
            self.unit_no2 = str(self.unit_no2).title()

    building_name2 = fields.Char(string="Building Name")

    @api.onchange('building_name2')
    def caps_building_name2(self):
        if self.building_name2:
            self.building_name2 = str(self.building_name2).title()

    street2 = fields.Char(string="Street")

    @api.onchange('street2')
    def caps_street2(self):
        if self.street2:
            self.street2 = str(self.street2).title()

    district2 = fields.Char(string="District/Barangay/Village")

    @api.onchange('district2')
    def caps_district2(self):
        if self.district2:
            self.district2 = str(self.district2).title()

    city2 = fields.Char(string="City")

    @api.onchange('city2')
    def caps_city2(self):
        if self.city2:
            self.city2 = str(self.city2).title()

    zip2 = fields.Char(string="Zip Code", size=4)

    @api.constrains('zip2')
    def _validate_zip2(self):
        for record in self:
            pattern = r'^\d{4}$'  # Modify the regular expression pattern according to your requirements
            if record.zip2 and not re.match(pattern, record.zip2):
                raise ValidationError('Invalid Zip Code!')

    landline2 = fields.Char(string="Telephone", help="This field includes a hyphen", size=16)

    @api.onchange('landline2')
    def onchange_landline2(self):
        for record in self:
            if record.landline2 and len(record.landline2) == 13:
                formatted_number = '-'.join([
                    record.landline2[:2],
                    record.landline2[2:6],
                    record.landline2[6:10],
                    record.landline2[10:]
                ])
                record.landline2 = formatted_number

    @api.constrains('landline2')
    def _check_landline2(self):
        for record in self:
            if record.landline2:
                if any(char.isalpha() and char != '-' for char in record.landline2):
                    raise ValidationError(
                        "Only numbers are allowed in the Telephone Number.")

    primary_contact_person = fields.Char(string="Primary Contact")

    @api.onchange('primary_contact_person')
    def caps_primary_contact_person(self):
        if self.primary_contact_person:
            self.primary_contact_person = str(self.primary_contact_person).title()

    @api.onchange('primary_contact_person')
    def _onchange_primary_contact_person(self):
        for record in self:
            if any(char.isdigit() for char in record.primary_contact_person):
                raise ValidationError("Numbers are not allowed in the Primary Contact Person.")

    mobile_number = fields.Char(string="Mobile No.")

    @api.constrains('mobile_number')
    def _validate_mobile_number(self):
        for record in self:
            pattern = r'^(?:\+63|0)\d{10}$'  # Modify the regular expression pattern according to your requirements
            if record.mobile_number and not re.match(pattern, record.mobile_number):
                raise ValidationError('Invalid mobile number format!')

    email_address = fields.Char(string="Email Address")
    principal_accounting_officer = fields.Char(string="Principal Accounting Officer")

    @api.onchange('principal_accounting_officer')
    def caps_principal_accounting_officer(self):
        if self.principal_accounting_officer:
            self.principal_accounting_officer = str(self.principal_accounting_officer).title()

    @api.onchange('principal_accounting_officer')
    def _onchange_principal_accounting_officer(self):
        for record in self:
            if any(char.isdigit() for char in record.principal_accounting_officer):
                raise ValidationError("Numbers are not allowed in this Field.")

    landline3 = fields.Char(string="Telephone", help="This field includes a hyphen", size=16)

    @api.onchange('landline3')
    def onchange_landline3(self):
        for record in self:
            if record.landline3 and len(record.landline3) == 13:
                formatted_number = '-'.join([
                    record.landline3[:2],
                    record.landline3[2:6],
                    record.landline3[6:10],
                    record.landline3[10:]
                ])
                record.landline3 = formatted_number

    @api.constrains('landline3')
    def _check_landline3(self):
        for record in self:
            if record.landline3:
                if any(char.isalpha() and char != '-' for char in record.landline3):
                    raise ValidationError(
                        "Only numbers are allowed in the Telephone Number.")

    mobile_number2 = fields.Char(string="Mobile No.")

    @api.constrains('mobile_number2')
    def _validate_mobile_number2(self):
        for record in self:
            pattern = r'^(?:\+63|0)\d{10}$'  # Modify the regular expression pattern according to your requirements
            if record.mobile_number2 and not re.match(pattern, record.mobile_number2):
                raise ValidationError('Invalid mobile number format!')

    email_address2 = fields.Char(string="Email Address")
    corporate_ids = fields.One2many(comodel_name='corporate.officer', inverse_name='client_profile_id',
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

    rdo_code = fields.Char(string="RDO Code", size=3)

    @api.constrains('rdo_code')
    def _validate_rdo_code(self):
        for record in self:
            pattern = r'^\d{3}$'  # Modify the regular expression pattern according to your requirements
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

    @api.onchange('psic_psoc')
    def onchange_psic_psoc(self):
        for record in self:
            if record.psic_psoc and len(record.psic_psoc) == 10:
                formatted_number = '-'.join([
                    record.psic_psoc[:4],
                    record.psic_psoc[4:10],
                ])
                record.psic_psoc = formatted_number

    @api.constrains('psic_psoc')
    def _check_psic_psoc(self):
        for record in self:
            if record.psic_psoc:
                if any(char.isalpha() and char != '-' for char in record.psic_psoc):
                    raise ValidationError(
                        "Only numbers are allowed in the PSIC/PSOC")

    ll_cas_permit_no = fields.Char(string="LL/CAS Permit No")

    @api.constrains('ll_cas_permit_no')
    def _check_ll_cas_permit_no(self):
        for record in self:
            if record.ll_cas_permit_no:
                if any(char.isalpha() and char != '-' for char in record.ll_cas_permit_no):
                    raise ValidationError(
                        "Only numbers are allowed in the LL/CAS Permit No.")

    ask = fields.Selection([('yes', 'Yes'), ('no', 'No')], default="no")
    registration_number = fields.Char(string="Registration No", size=13)

    @api.onchange('registration_number')
    def set_upper(self):
        self.registration_number = str(self.registration_number).upper()
        return

    registration_date_sec = fields.Date('Date')
    trade_name = fields.Char(string="Trade Name")

    # @api.onchange('name')
    # def copy_client_name(self):
    #     for record in self:
    #         record.trade_name = record.name

    @api.onchange('trade_name')
    def set_upper(self):
        self.trade_name = str(self.trade_name).upper()
        return

    date_per_law = fields.Char(string="Date per By-Laws")
    actual_date_meeting = fields.Date('date')
    ask_1 = fields.Selection([('yes', 'Yes'), ('no', 'No')], default="no")
    ask_2 = fields.Text(string="If Yes what type of security is the Company permit to sell?")
    capitalization_ids = fields.One2many(comodel_name='capitalization.share', inverse_name='capitalization_id',
                                         string="Class of Shares")
    capital_sole_proprietor_ids = fields.One2many(comodel_name='capital.sole.proprietor',
                                                  inverse_name='capital_sole_proprietor_id',
                                                  string="Capital Sole Proprietor")
    capital_general_partner_ids = fields.One2many(comodel_name='capital.general.partnership',
                                                  inverse_name='capital_general_partner_id',
                                                  string="Capital General Partnership")
    capital_general_professional_partner_ids = fields.One2many(comodel_name='capital.general.professional.partnership',
                                                               inverse_name='capital_general_professional_partner_id',
                                                               string="Capital General Partnership")
    capital_domestic_ids = fields.One2many(comodel_name='capital.domestic.nsnp', inverse_name='capital_domestic_id',
                                           string="Capital Domestic NSNP")
    capital_foreign_corp_ids = fields.One2many(comodel_name='capital.foreign.corp',
                                               inverse_name='capital_foreign_corp_id',
                                               string="Capital Foreign Corporation")
    capital_foreign_nsnp_ids = fields.One2many(comodel_name='capital.foreign.nsnp.corp',
                                               inverse_name='capital_foreign_nsnp_id', string="Capital Foreign NSNP")
    capital_roqh_foreign_corp_ids = fields.One2many(comodel_name='capital.roqh.foreign.corp',
                                                    inverse_name='capital_roqh_foreign_corp_id',
                                                    string="Capital ROQH Foreign")
    capital_representative_office_ids = fields.One2many(comodel_name='capital.representative.office',
                                                        inverse_name='capital_representative_office_id',
                                                        string="Capital Representative Office")
    ask_3 = fields.Selection([('yes', 'Yes'), ('no', 'No')], default="no")
    bureau_of_custom = fields.Boolean(string="Bureau of Customs")
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
    attachment = fields.Many2many('ir.attachment', 'attachment_rel', 'pro_id', 'attach_id', string='Attachments', )
    attachment_fname = fields.Char(string="Attachment Filename")
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
