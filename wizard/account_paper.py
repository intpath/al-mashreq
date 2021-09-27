from operator import index
from odoo import models, fields, api
from odoo.exceptions import UserError
class AccountPaper(models.TransientModel):
	_name = "account.paper"

	from_date = fields.Datetime("From Date")
	to_date = fields.Datetime("To Date")

	def format_account_move_data(self):
		args = [('state', '=', 'posted')]
		if self.from_date:
			args += [('date', '>=', self.from_date)]
		if self.to_date:
			args += [('date', '<=', self.to_date)]

		account_moves = self.env['account.move'].search(args)

		response = []
		index = 1
		for move in account_moves:
			credit = sum( move.line_ids.mapped('credit') )
			credit_account_id = move.line_ids.filtered(lambda line: line.credit > 0)[0].account_id
			debit = sum( move.line_ids.mapped('debit') )
			debit_account_id = move.line_ids.filtered(lambda line: line.debit > 0)[0].account_id

			response.append((
				move.date.strftime("%Y/%m/%d"),
				debit_account_id.name,
				debit_account_id.code,
				credit_account_id.name,
				credit_account_id.code,
				move.name,
				dict(move._fields['bond_type'].selection).get(move.bond_type),
				move.bond_number,
				index,
				move.amount_total_signed,
				credit_account_id.group_id.display_name if credit_account_id.group_id.display_name else '',
				credit,
				debit_account_id.group_id.display_name if debit_account_id.group_id.display_name else '',
				debit,
			))
			index += 1

		return response
