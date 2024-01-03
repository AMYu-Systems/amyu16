from odoo import models, fields, api


class MainView(models.Model):
    _name = 'main.view'
    _description = "Monitoring Viewer"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Client Name")

    @api.onchange('name')
    def caps_name(self):
        if self.name:
            self.name = str(self.name).upper()

    user_id = fields.Many2one(string="Associate", comodel_name='res.users', default=lambda self: self.env.user,
                              tracking=True)
    supervisor_id = fields.Many2one(string="Supervisor", comodel_name='res.users')
    manager_id = fields.Many2one(string="Manager", comodel_name='res.users')
    partner_id = fields.Many2one(string="Partner", comodel_name='res.users')
    state = fields.Selection([('preparation', 'Preparation'), ('checking', 'Checking'), ('review', 'Review'),
                              ('initial_approval', 'Init. Approval'), ('proofread', 'Proofread'),
                              ('final_checking', 'FNL Checking'), ('final_review', 'FNL Review'),
                              ('final_approval', 'FNL Approval'), ('final_proofread', 'FNL Proofread'),
                              ('iar_review', 'IAR Review'), ('printing', 'Print'), ('sorting', 'Sort'),
                              ('qcc', 'Quality Control Check'), ('filing', 'File'), ('filed', 'Filed')],
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
    revision = fields.Selection([('process', 'In Progress'), ('revision', 'Revision'), ('done', 'Done')],
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

    # PRINT
    print_itr_form = fields.Boolean(string="ITR FORM", tracking=True)
    print_cs = fields.Boolean(string="Cover Sheet", tracking=True)
    print_iar = fields.Boolean(string="IAR", tracking=True)
    print_fs = fields.Boolean(string="SMR for FS", tracking=True)
    print_itr = fields.Boolean(string="SMR for ITR", tracking=True)
    print_afs = fields.Boolean(string="AFS", tracking=True)
    print_form1709 = fields.Boolean(string="1709 Form", tracking=True)
    print_others = fields.Boolean(string="Other Attachment (specify)", tracking=True)
    print_text_others = fields.Char()
    # SORT
    sort_itr_form = fields.Boolean(string="ITR FORM", tracking=True)
    sort_cs = fields.Boolean(string="Cover Sheet", tracking=True)
    sort_iar = fields.Boolean(string="IAR", tracking=True)
    sort_fs = fields.Boolean(string="SMR for FS", tracking=True)
    sort_itr = fields.Boolean(string="SMR for ITR", tracking=True)
    sort_afs = fields.Boolean(string="AFS", tracking=True)
    sort_form1709 = fields.Boolean(string="1709 Form", tracking=True)
    sort_others = fields.Boolean(string="Other Attachment (specify)", tracking=True)
    sort_text_others = fields.Char()
    # Q.C.C
    qcc_itr_form = fields.Boolean(string="ITR FORM", tracking=True)
    qcc_cs = fields.Boolean(string="Cover Sheet", tracking=True)
    qcc_iar = fields.Boolean(string="IAR", tracking=True)
    qcc_fs = fields.Boolean(string="SMR for FS", tracking=True)
    qcc_itr = fields.Boolean(string="SMR for ITR", tracking=True)
    qcc_afs = fields.Boolean(string="AFS", tracking=True)
    qcc_form1709 = fields.Boolean(string="1709 Form", tracking=True)
    qcc_others = fields.Boolean(string="Other Attachment (specify)", tracking=True)
    qcc_text_others = fields.Char()
    # BIR FILING
    bir_itr_form = fields.Boolean(string="ITR FORM", tracking=True)
    bir_trrc = fields.Boolean(string="TRRC", tracking=True)
    bir_iar = fields.Boolean(string="IAR", tracking=True)
    bir_itr = fields.Boolean(string="SMR for ITR", tracking=True)
    bir_afs = fields.Boolean(string="AFS", tracking=True)
    bir_form1709 = fields.Boolean(string="1709 Form", tracking=True)
    bir_sawt = fields.Boolean(string="SAWT", tracking=True)
    bir_sawt_validation = fields.Boolean(string="SAWT Validation", tracking=True)
    bir_others = fields.Boolean(string="Other Attachments (specify)", tracking=True)
    bir_text_others = fields.Char()
    # SEC FILING
    sec_eafs = fields.Boolean(string="EAFS Submission Receipt", tracking=True)
    sec_iar = fields.Boolean(string="IAR", tracking=True)
    sec_fs = fields.Boolean(string="SMR for FS", tracking=True)
    sec_afs = fields.Boolean(string="AFS", tracking=True)
    sec_sws = fields.Boolean(string="SWS", tracking=True)
