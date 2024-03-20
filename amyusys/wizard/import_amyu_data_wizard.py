from odoo import fields, models, api


class ImportAmyuDataWizard(models.TransientModel):
    _name = 'import.amyu.data.wizard'
    _description = "Allows import of data according to models of AMYU modules"
    
    excel_file = fields.Binary()
    csv_file = fields.Binary()
    
    def process_import(self):
        print('AAAAAAAAAAAAAAAA')
        print('AAAAAAAAAAAAAAAA')
        print('AAAAAAAAAAAAAAAA')
        print('AAAAAAAAAAAAAAAA')
        return True
    