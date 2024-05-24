from odoo import models, fields, api
from odoo.exceptions import ValidationError
from ..report.collection_report import CollectionReportXlsx

class CollectionReport(models.TransientModel):
    _name = 'bcs.collection_report'

    date_start = fields.Date()
    date_end = fields.Date(default=lambda self: fields.Date.today())
    
    def filename(self) -> str:
        has_both_dates = self.date_start and self.date_end
        name = f'{fields.Date.today()} Collection Report '
        if has_both_dates:
            name += f'({self.date_start}-{self.date_start})'
        else:
            name += '(all)'
        return name
    
    
    def export_collection_report(self):
        
        # validate date
        no_dates = not self.date_start and not self.date_end
        has_both_dates = self.date_start and self.date_end
        if not no_dates and not has_both_dates:
            return None
        
        filters = [('state', '=', 'approved')]
        if has_both_dates:
            filters.append(('date_collected','>=', self.date_start))
            filters.append(('date_collected','<=', self.date_end))
         
        data = self.env['bcs.collection'].search(filters, order="transaction desc")
        CollectionReportXlsx.generate_xlsx_report(data=data, filename=self.filename())
        return