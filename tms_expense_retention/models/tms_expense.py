# -*- coding: utf-8 -*-
# Copyright 2016, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class TmsExpense(models.Model):
    _inherit = 'tms.expense'

    @api.multi
    def get_retention(self):
        for rec in self:
            obj_retention = self.env['tms.retention']
            retentions = [x for x in obj_retention.search([])]
            for retention in retentions:
                value = 0.0
                product = self.env['product.product'].search(
                    [('id', '=', retention.product_id.id),
                     ('apply_for_retention', '=', True)])
                if retention.employee_ids:
                    if rec.employee_id in retention.employee_ids:
                        if retention.retention_type == 'days':
                            days = int(rec.travel_days.split('D')[0])
                            value = retention.factor * days
                        else:
                            value = rec.amount_salary * retention.factor
                else:
                    value = retention.factor * days
                if value > 0.0:
                    rec.expense_line_ids.create({
                        'name': retention.name,
                        'expense_id': rec.id,
                        'line_type': "salary_retention",
                        'product_qty': 1.0,
                        'product_uom_id': product.uom_id.id,
                        'product_id': product.id,
                        'unit_price': value,
                        'control': True
                    })

    @api.multi
    def get_travel_info(self):
        for rec in self:
            res = super(TmsExpense, self).get_travel_info()
            rec.get_retention()
            return res
