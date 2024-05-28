from datetime import date
from odoo import models


# =============================
import logging
_logger = logging.getLogger(__name__)


def test_with_logger(data: any = "Debug Message", warn: bool = False) -> None:
    """ Outputs a debug message in the odoo log file, 5 times in a row """
    method = _logger.info if not warn else _logger.warning
    for _ in range(5):
        method(data)
# =============================


class CollectionReportXlsx(models.AbstractModel):
    _name = 'report.bcs.collection_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    FIELDS = [
        'transaction', # A
        'paid_by_id', # B
        # 'billing_ids',
        'billing_ids.transaction',
        'billing_ids.date_billed',
        'billing_ids.services_id',
        'billing_ids.client_id',
        'billing_ids.amount',
        'collected_by',
        'date_collected',
        'depository_bank',
        'payment_mode',
        'bank',
        'amount',
        'remarks',
    ]
    
    BILLING_COLUMN_NAMES = {
        'billing_ids.transaction': 'Billing ID',
        'billing_ids.date_billed': 'Date Billed',
        'billing_ids.services_id': 'Type of Services',
        'billing_ids.client_id': 'Paid for (Client)',
        'billing_ids.amount': 'Billing Amount',
    }


    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet('Collection Report')
        font12 = workbook.add_format({'font_size': 12})
        number = workbook.add_format({'font_size': 12, 'num_format': '#,##0.00'})
        # sheet.set_column('D:D', 12)
        
        # Write the column names
        for col, col_name in enumerate(self._column_names()):
            header = workbook.add_format({'font_size': 12, 'bold': True})
            sheet.write(0, col, col_name, header)
        
        # Write the data
        row = 1
        col_idx: dict = self._column_index()
        for collection in data['collections']:
            billing_ids_list = collection['billing_ids']
            billing_ids = self.env['bcs.billing'].search([('id', 'in', billing_ids_list)])
            # Write collection fields
            for field in self.FIELDS:
                if field.startswith('billing_ids'): continue
                value, style = self._format_field_value(workbook, collection, field)
                sheet.write(row, col_idx[field], value, style)
            # Write billing fields
            for billing in billing_ids:
                for field in self.FIELDS:
                    if not field.startswith('billing_ids'): continue
                    billing_field = field.split('.')[-1]
                    value, style = self._format_billing_field_value(workbook, billing, billing_field)
                    sheet.write(row, col_idx[field], value, style)
                row += 1
                

    
    def _column_index(self) -> dict:
        index = {}
        for idx, field in enumerate(self.FIELDS):
            index[field] = idx
        return index
                
                
    def _column_names(self):
        collection_model = self.env['bcs.collection']
        
        col_names = []
        for field in self.FIELDS:
            if field.startswith('billing_ids'):
                col_name = self.BILLING_COLUMN_NAMES[field]
            else:
                col_name = collection_model.fields_get([field])[field]['string']
            col_names.append(col_name)
        
        return col_names
    

    def _format_field_value(self, workbook, collection, field:str):
        font12 = workbook.add_format({'font_size': 12})
        number = workbook.add_format({'font_size': 12, 'num_format': '#,##0.00'})
        
        if field in collection and not collection[field]:
            return ('', font12)
        
        if field in ['paid_by_id', 'collected_by']: # Many2one field
            return (collection[field][1], font12)
        elif field in ['amount']: # Needs financial format
            return (collection[field], number)
        else:
            return (str(collection[field]), font12)
        
    
    def _format_billing_field_value(self, workbook, billing, field:str):
        font12 = workbook.add_format({'font_size': 12})
        number = workbook.add_format({'font_size': 12, 'num_format': '#,##0.00'})
        
        value = getattr(billing, field)
        if not value:
            return ('', font12)

        if field == 'services_id':
            service_names = ", ".join(value.mapped('name'))
            return (service_names, font12)
        elif field == 'client_id':
            return (value.name, font12)
        elif field == 'amount':
            return (value, number)
        else:
            return (str(value), font12)
        
        
