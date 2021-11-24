# -*- coding: utf-8 -*-

from typing import Text
from odoo import models, fields, api


class AccountAccount(models.Model):
    _inherit = "account.account"

    exclude_from_payment_spending_report = fields.Boolean("Exclude from سند الصرف", copy=False, groups="base.group_no_one")
