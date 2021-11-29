# -*- coding: utf-8 -*-

from typing import Text
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    BOND_SELECTION = [
        ('check', 'صك'),
        ('payment_recieve', 'مستند القبض'),
        ('payment_paid', 'مستند الدفع'),
        ('payment_document', 'مستند القيد')
    ]

    bond_type = fields.Selection(BOND_SELECTION, "نوع السند", readonly=True, states={'draft': [('readonly', False)]})
    bond_number = fields.Char("رقم السند", readonly=True, states={'draft': [('readonly', False)]})

    written_amount = fields.Char("المجموع كتابة")

    free_text = fields.Text("وصف")


    def add_comma(self, value):
        num = int(value) 
        return f"{num: ,}"


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    
    duplicate_name = fields.Text(string="Duplicate Name", compute="_on_change_name")
    extra_text = fields.Text(string="Extra Text")

    @api.onchange('name')
    def _on_change_name(self):
        for line in self:
            line.duplicate_name = line.name
