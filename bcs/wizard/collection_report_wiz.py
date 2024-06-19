from odoo import models, fields, api
from odoo.exceptions import ValidationError
from ..report.collection_report import CollectionReportXlsx


class CollectionReportWiz(models.TransientModel):
    _name = 'collection.report.wizard'
    
    
    @api.onchange('date_start', 'date_end')
    def _onchange_dates(self):
        today = fields.Date.today()
        
        # validate
        if self.date_start and self.date_start > today:
            raise ValidationError('Invalid Start Date.')
        if self.date_end and self.date_end > today:
            raise ValidationError('Invalid End Date.')
        if self.date_start and self.date_end and self.date_end < self.date_start:
            self.date_start = self.date_end.replace(day=1)
            raise ValidationError('Invalid Date Range.')
            
        ds = self.date_start
        de = self.date_end
        name = f'{today} Collection Report'
        if ds and de:
            name += f' ({ds} to {de})'
        elif not (ds or de):
            name += ' (all)'
        self.report_file_name = name
        
        
    report_file_name = fields.Char(default=_onchange_dates)
    
    def _default_date_start(self):
        today = fields.Date.today()
        first = today.replace(day=1)
        return first    
    
    date_start = fields.Date(default=_default_date_start)
    date_end = fields.Date(default=lambda self: fields.Date.today())
            
    # @api.multi
    def export_collection_report(self):
        
        # validate date
        if self.date_start and self.date_start > fields.Date.today() \
            or self.date_end and self.date_end > fields.Date.today():
            raise ValidationError('Invalid Start or End Date.')
        if self.date_start and self.date_end and self.date_start > self.date_end:
            raise ValidationError('Invalid Date Range.')

        domain = [('state', '=', 'approved')]
        if self.date_start:
            domain.append(('date_collected', '>=', self.date_start))
        if self.date_end:
            domain.append(('date_collected', '<=', self.date_end))

        collections = self.env['bcs.collection'].search_read(
            domain, order="transaction desc")
        data = {'collections': collections}
        
        report = self.env.ref('bcs.collection_report_xlsx_rec_id')
        # report.print_report_name = self.report_file_name
        return report.report_action(self, data=data)
