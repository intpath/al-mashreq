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


class AccountPayment(models.Model):
    _inherit = "account.payment"
    pay_type = fields.Selection([('cash', 'نقد'), ('check', 'صك')])
