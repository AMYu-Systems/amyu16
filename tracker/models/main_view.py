from odoo import models, fields, api


class MainView(models.Model):
    _name = 'main.view'
    _description = "Monitoring Viewer"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Client Name", required=True)

    @api.onchange('name')
    def caps_name(self):
        if self.name:
            self.name = str(self.name).upper()

    user_id = fields.Many2one(string="Associate", comodel_name='res.users', default=lambda self: self.env.user,
                              tracking=True)
    supervisors_id = fields.Many2one(string="Supervisor", comodel_name='team.supervisor')
    managers_id = fields.Many2one(string="Manager", comodel_name='team.manager')
    cluster_id = fields.Many2one(string="Partner", comodel_name='group.cluster')
    state = fields.Selection([('preparation', 'Preparation'), ('checking', 'Checking'), ('review', 'Review'),
                              ('initial_approval', 'Init. Approval'), ('proofread', 'Proofread'),
                              ('final_checking', 'FNL Checking'), ('final_review', 'FNL Review'),
                              ('final_approval', 'FNL Approval'), ('final_proofread', 'FNL Proofread'),
                              ('iar_review', 'IAR Review'), ('printing', 'Printing'), ('sorting', 'Sorting'),
                              ('qcc', 'Quality Control Check'), ('filing', 'Filing'), ('filed', 'Filed')],
                             string="Status", default='preparation', tracking=True, group_expand='_expand_states',
                             index=True)

    def action_preparation(self):
        self.state = 'preparation'

    def action_checking(self):  # send to review
        self.state = 'checking'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_review(self):  # send to initial
        self.state = 'review'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_initial(self):
        self.state = 'initial_approval'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_proofread(self):
        self.state = 'proofread'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_final_checking(self):
        self.state = 'final_checking'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_final_review(self):
        self.state = 'final_review'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_final_approval(self):
        self.state = 'final_approval'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_final_proofread(self):
        self.state = 'final_proofread'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_iar_review(self):
        self.state = 'iar_review'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_printing(self):
        self.state = 'printing'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_sorting(self):
        self.state = 'sorting'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_qcc(self):
        self.state = 'qcc'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_filing(self):
        self.state = 'filing'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_filed(self):
        self.state = 'filed'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    date_start = fields.Datetime(string="Date Start", default=lambda self: fields.datetime.now())
    date_end = fields.Datetime(string="Date End")
    total_time = fields.Integer(string="Total Time", compute='_compute_total_time', store=True)
    revision = fields.Selection([('process', 'In Progress'), ('revision', 'Revision'), ('done', 'Proceed')],
                                string="Status", tracking=True,
                                default='process')

    def action_proceed(self):
        self.revision = 'done'

    @api.depends('date_start', 'date_end')
    def _compute_total_time(self):
        for record in self:
            if record.date_start and record.date_end:
                # Compute the time difference between start_date and end_date
                time_delta = record.date_end - record.date_start
                # Extract total seconds from the time delta
                total_seconds = time_delta.total_seconds()
                # Convert seconds to hours
                total_hours = total_seconds / 3600
                # Update the total_time field
                record.total_time = total_hours
            else:
                record.total_time = 0.0

    # LABEL
    label_note_ids = fields.Many2many(string="Label", comodel_name='label.maintenance', inverse_name='label_id',
                                      tracking=True)
    label_printer_ids = fields.Many2many(string="Printer Checklist", comodel_name='label.printer',
                                         inverse_name='printer_id', tracking=True)
    label_sorter_ids = fields.Many2many(string="Sorter Checklist", comodel_name='label.sorter',
                                        inverse_name='sorter_id', tracking=True)
    label_qcc_ids = fields.Many2many(string="Quality Check Control Checklist",
                                     comodel_name='label.qcc', inverse_name='qcc_id', tracking=True)
    label_bir_ids = fields.Many2many(string="B.I.R Checklist", comodel_name='label.bir', inverse_name='bir_id',
                                     tracking=True)
    label_sec_ids = fields.Many2many(string="S.E.C Checklist", comodel_name='label.sec', inverse_name='sec_id',
                                     tracking=True)
