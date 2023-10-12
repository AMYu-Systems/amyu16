from odoo import fields, models


class TaxType(models.Model):
    _name = 'tax.type'
    _description = "Tax Selection"

    name = fields.Char(string="Tax")
    select_tax_types = fields.Selection([('income_tax', 'Income Tax'), ('excise_tax', 'Excise Tax'),
                                         ('value_added_tax ', 'Value-added Tax'),
                                         ('withholding_tax_expanded', 'Withholding Tax - Expanded'),
                                         ('withholding_tax_compensation', 'Withholding Tax - Compensation'),
                                         ('withholding_tax_final', 'Withholding Tax - Final'),
                                         ('registration_fee', 'Registration Fee'),
                                         ('other_percentage_tax', 'Other Percentage Tax')])
