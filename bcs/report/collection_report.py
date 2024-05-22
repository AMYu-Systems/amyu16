from odoo import models
import logging

_logger = logging.getLogger(__name__)


# Test
def test_with_logger(data: any = "Debug Message", warn: bool = False) -> None:
    """
        Outputs a debug message in the odoo log file, 5 times in a row
    """
    method = _logger.info if not warn else _logger.warning
    for _ in range(5):
        method(data)
        
class CollectionReportXlsx(models.AbstractModel):
    _name = 'report.bcs.collection_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        # report_name = obj.name
        sheet = workbook.add_worksheet('Report')
        bold = workbook.add_format({'font_size': 12})
        
        # sheet.write(0, 0, obj.name, bold)