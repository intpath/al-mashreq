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

	bond_type = fields.Selection(BOND_SELECTION, "نوع السند")
	bond_number = fields.Integer("رقم السند")