# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    BOND_SELECTION = [
        ('check', 'صك'),
        ('payment_recieve', 'مستند القبض'),
        ('payment_paid', 'مستند الدفع'),
        ('payment_document', 'مستند القيد')
    ]

    bond_type = fields.Selection(BOND_SELECTION, "نوع السند", readonly=True, states={
                                 'draft': [('readonly', False)]})
    bond_number = fields.Integer("رقم السند", readonly=True, states={
                                 'draft': [('readonly', False)]})

class AccountAccount(models.Model):
	_inherit = "account.account"

	exclude_from_payment_spending_report = fields.Boolean("Exclude from سند الصرف", copy=False, groups="base.group_no_one")

class AccountPayment(models.Model):
	_inherit = "account.payment"

	real_partner_due = fields.Monetary(
		string="مستحق الزبون/المجهز", compute="_compute_partner_due", currency_field="company_currency_id")
	company_currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id.id, readonly=True, copy=False)
	recieve_type = fields.Selection([('cash', 'نقد'), ('check', 'صك')], string="نوع السداد")

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

class Student(models.Model):
    _inherit = "res.partner"

    student_id = fields.Many2one(
        "op.student", string="Related Student", compute="_compute_student_id")

    def _compute_student_id(self):
        for record in self:
            student_id = self.env['op.student'].search(
                [('partner_id', '=', record.id)])
            record.student_id = student_id.id
