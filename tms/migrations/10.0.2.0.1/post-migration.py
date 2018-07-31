# -*- coding: utf-8 -*-
import logging
from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def change_accounts_multicompany(cr):
    cr.execute('''
        SELECT id, tms_loan_account_id, tms_expense_negative_account_id,
        tms_advance_account_id FROM hr_employee;
        ''')
    records = cr.dictfetchall()
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        _logger.info('Redefine accounts to multicompany.')
        for rec in records:
            env['hr.employee'].browse(rec['id']).write({
                'tms_loan_account_id': rec['tms_loan_account_id'],
                'tms_expense_negative_account_id':
                    rec['tms_expense_negative_account_id'],
                'tms_advance_account_id': rec['tms_advance_account_id'],
            })


def migrate(cr, version):
    change_accounts_multicompany(cr)
    cr.execute('''
        ALTER TABLE hr_employee
        DROP COLUMN tms_loan_account_id,
        DROP COLUMN tms_expense_negative_account_id,
        DROP COLUMN tms_advance_account_id;
        ''')
