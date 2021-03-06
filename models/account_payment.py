# -*- coding: utf-8 -*-

from typing import Text
from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = "account.payment"

    BOND_SELECTION = [
        ('check', 'صك'),
        ('payment_recieve', 'مستند القبض'),
        ('payment_paid', 'مستند الدفع'),
        ('payment_document', 'مستند القيد')
    ]
    bond_type = fields.Selection(BOND_SELECTION, "نوع السند")
    bond_number = fields.Char("رقم السند")


    free_text = fields.Text("وصف")

    real_partner_due = fields.Monetary(string="مستحق الزبون/المجهز", compute="_compute_partner_due", currency_field="company_currency_id")
    company_currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id.id, readonly=True, copy=False)
    recieve_type = fields.Selection([('cash', 'نقد'), ('check', 'صك')], string="نوع السداد")
    department = fields.Many2one('op.course', string="Dept", compute="_compute_department", store=True)
    stage = fields.Selection(string="Stage", related="partner_id.student_id.stage", store=True)
    category = fields.Many2one(string="Category", related="partner_id.student_id.category_id", store=True)
    destination_account_id = fields.Many2one(domain="")
    void = fields.Char("بطال؟", readonly=True, compute="_is_void")
    written_amount = fields.Char("المجموع كتابة")
    canceled_before = fields.Boolean(
        "Canceled Before?", compute="_canceled_before")
    can_edit_date = fields.Boolean(
        "Can Edit Date?", compute="_can_edit_date")


    @api.constrains('state')
    def _is_void(self):
        for record in self:
            # record.void = "بطال" if record.state == "cancel" else ""
            if record.state == "cancel":
                record.void = "بطال"
            else:
                record.void = ""
            if record.state == "cancel" and not record.amount == 0:
                record.message_post(
                    body=f"Paymemt Canceled, Amount was: {record.amount} {record.currency_id.symbol}")
                record.amount = 0

    @api.depends('state')
    def _canceled_before(self):
        for record in self:
            record.canceled_before = False
            if record.state == "cancel":
                record.canceled_before = True
                
    def _can_edit_date(self):
        for record in self:
            if record.env.user.has_group('account.group_account_manager'):
                record.can_edit_date = True
            else:
                record.can_edit_date = False

    @api.depends('partner_id')
    def _compute_department(self):
        for record in self:
            course_id = self.env['op.student.course'].search(
                    [('student_id', '=', record.partner_id.student_id.id)])
            if course_id:
                temp = course_id[0]
                for line in course_id:
                    if temp.batch_id.start_date < line.batch_id.start_date:
                        temp = line
                record.department = temp.course_id
            else:
                record.department = False
                

    @api.onchange('partner_id')
    def _compute_partner_due(self):
        account_partner_ledger = self.env['account.partner.ledger'].with_context({'default_partner_id': self.partner_id.id})
        options = account_partner_ledger._get_options()
        options['partner_ids'] = [self.partner_id.id]
        lines = account_partner_ledger._get_partner_ledger_lines(options)
        if self.env.company.currency_id.position == 'before':
            total_balance = float(lines[-1]['columns'][-1]['name'].split()[-1].replace(',', ''))
        else:
            total_balance = float(lines[-1]['columns'][-1]['name'].split()[-2].replace(',', ''))

        self.real_partner_due = total_balance

    def get_latest_rec(self, records):
        tep = self.env['op.student.course']
        for rec in records:
            if not tep:
                tep = rec

            if tep.batch_id.start_date < rec.batch_id.start_date:
                tep = rec

        return tep
    def add_comma(self, value):
        num = int(value) 
        return f"{num: ,}"

    # @api.depends('state')
    # def amount_zero_after_cancel(self):
    #     for record in self:
    #         if record.state == "cancel":
    #             record.message_post(body=f"Paymemt Canceled, Amount was: {record.amount} {record.currency_id.symbol}")
    #             record.amount = 0 
    #         else:
    #             pass

    def action_advisor_cancel(self):
        ''' draft -> cancelled '''
        if self.state == 'draft':
            self.move_id.button_draft()
        self.move_id.button_cancel()
