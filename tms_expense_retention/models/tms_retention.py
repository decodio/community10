# -*- coding: utf-8 -*-
# Copyright 2016, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, exceptions, fields, models


class TmsRetention(models.Model):
    _name = "tms.retention"
    _description = "Tms Retention"

    name = fields.Char(
    )
    retention_type = fields.Selection(
        [('days', 'Days'),
         ('salary', 'Salary'), ],
        default='days')
    factor = fields.Float()
    mixed = fields.Boolean()
    fixed_amount = fields.Float()
    employee_ids = fields.Many2many('hr.employee')
    product_id = fields.Many2one('product.product')

    @api.constrains('product_id')
    def unique_product(self):
        for rec in self:
            product = rec.search([
                ('product_id', '=', rec.product_id.id),
                ('id', '!=', rec.id)])
            if product:
                raise exceptions.ValidationError(
                    _('Only there must be a product "' +
                        product.product_id.name + '"'))
