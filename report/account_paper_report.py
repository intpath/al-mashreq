
from odoo import models
from odoo.exceptions import UserError

class AccountPaperReport(models.AbstractModel):
    _name = "report.report_xlsx.account_paper_report"
    _inherit = "report.report_xlsx.abstract"
    _description = "Account Paper Report"


    def generate_xlsx_report(self, workbook, data, wizard):
        sheet = workbook.add_worksheet("Report")

        #  Setting Direction and columns Width
        sheet.right_to_left()
        sheet.set_column("A:A", 12)
        sheet.set_column("B:B", 21)
        sheet.set_column("D:D", 21)
        sheet.set_column("F:F", 24)
        sheet.set_column("G:G", 11)
        sheet.set_column("I:I", 5)
        sheet.set_column("J:J", 17)
        sheet.set_column("K:K", 25)
        sheet.set_column("L:L", 17)
        sheet.set_column("M:M", 25)
        sheet.set_column("N:N", 17)

        # Headers Style
        header_style = workbook.add_format({
            "bg_color": "#63CACF",
            "bold": True,
            'text_wrap': True,
            "valign": "vcenter",
            "align": "center",
            "font_size": 11,
            "border": 1,
        })
        HEADERS_ROW = [
            "التاريخ",
            "من" ,
            "رقم الدليل",
            "الى",
            "رقم الدليل", 
            "التفاصيل",
            "نوع السند",
            "رقم السند",
            "الترقيم",
            "المبلغ العام",
            "من",
            "من رقم الدليل (المبلغ)",
            "الى",
            "الى رقم الدليل (المبلغ)",
            ]
        sheet.write_row('A1', HEADERS_ROW, header_style)

        # Insterting Data
        data = wizard.format_account_move_data()
        index = 2
        for row in data:
            sheet.write_row(f'A{index}', row)
            index += 1