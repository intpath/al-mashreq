# -*- coding: utf-8 -*-

from typing import Text
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    student_id = fields.Many2one("op.student", string="Related Student", compute="_compute_student_id")

    def _compute_student_id(self):
        for record in self:
            student_id = self.env['op.student'].search(
                [('partner_id', '=', record.id)])
            record.student_id = student_id.id
