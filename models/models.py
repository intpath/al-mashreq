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
    recieve_type = fields.Selection(
        [('cash', 'نقد'), ('check', 'صك')], string="نوع السداد")

    def get_latest_rec(self, records):
        for rec in records:
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


class Stage(models.Model):
    _inherit = 'op.student'

    stage = fields.Selection([('first', 'الاولى'), ('second', 'الثانية'), ('third', 'الثالثه'), (
        'fourth', 'الرابعة'), ('fifth', 'الخامسة'), ('sixth', 'السادسة')], string="المرحلة")
