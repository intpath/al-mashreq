# -*- coding: utf-8 -*-
{
    'name': "Al-Mashreq University",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'author': "Integerated Path",
    'website': "https://www.int-path.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '14.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'account_accountant', 'report_xlsx'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'report/payment_report.xml',
        'report/account_move_report.xml',
        'report/report_actions.xml',
        'wizard/account_paper_view.xml',
        'report/report_layout.xml',
    ],
}
