from odoo import fields, models
from datetime import datetime


class TimeSummary(models.Model):
    _name = "summary.of.time"
    _description = "Summary of Time Wizard"

    from_date = fields.Date(string="From", required=True)
    to_date = fields.Date(string="To", required=True)

    def button_export_xls(self):
        company_obj = self.env.company
        company_id = company_obj.id
        inet_host = company_obj.inet_host
        inet_folder = company_obj.inet_folder
        from_date = self.from_date.strftime("Date(%Y,%m,%d)")
        to_date = self.to_date.strftime("Date(%Y,%m,%d)")
        url = inet_host + "/?report=" + inet_folder + \
              "/dtr_time_summary.rpt&init=xlsx&prompt0=" + str(company_id) + \
              "&prompt1=" + from_date + "&prompt2=" + to_date
        return {'name': 'Summary of Time',
                'res_model': 'ir.actions.act_url',
                'type': 'ir.actions.act_url',
                'target': 'new',
                'url': url
                }
        return

    def button_preview_report(self):
        company_obj = self.env.company
        company_id = company_obj.id
        inet_host = company_obj.inet_host
        inet_folder = company_obj.inet_folder
        from_date = self.from_date.strftime("Date(%Y,%m,%d)")
        to_date = self.to_date.strftime("Date(%Y,%m,%d)")
        url = inet_host + "/?report=" + inet_folder + \
              "/dtr_time_summary.rpt&init=pdf&prompt0=" + str(company_id) + \
              "&prompt1=" + from_date + "&prompt2=" + to_date
        return {'name': 'Summary of Time',
                'res_model': 'ir.actions.act_url',
                'type': 'ir.actions.act_url',
                'target': 'new',
                'url': url
                }
