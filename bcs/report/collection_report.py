from datetime import date
from odoo import models

try:
   from odoo.tools.misc import xlsxwriter
except ImportError:
   import xlsxwriter


# =============================
import logging
_logger = logging.getLogger(__name__)
def test_with_logger(data: any = "Debug Message", warn: bool = False) -> None:
    """ Outputs a debug message in the odoo log file, 5 times in a row """
    method = _logger.info if not warn else _logger.warning
    for _ in range(5):
        method(data)
# =============================
  
        
class CollectionReportXlsx():

    COLUMNS = [
        'transaction',
        'paid_by_id',
        'billing_ids',
        'payment_collection',
        'collected_by',
        'date_collected',
        'depository_bank',
        'payment_bank',
        'bank',
        'amount',
        'remarks',
    ]
        
    @staticmethod
    def generate_xlsx_report(data, filename):
        # report_name = obj.name
        sheet = workbook.add_worksheet('Report')
        bold = workbook.add_format({'font_size': 12})
        
        # sheet.write(0, 0, obj.name, bold)