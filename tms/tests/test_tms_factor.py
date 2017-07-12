# -*- coding: utf-8 -*-
# Copyright 2016, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestTmsFactor(TransactionCase):

    def setUp(self):
        super(TestTmsFactor, self).setUp()
        self.factor = self.env['tms.factor']

    def test_10_tms_factor_onchange_factor_type(self):
        factor_type_list = [
            ['', 'name'],
            ['distance', 'Distance Route (Km/Mi)'],
            ['distance_real', 'Distance Real (Km/Mi)'],
            ['weight', 'Weight'],
            ['travel', 'Travel'],
            ['qty', 'Quantity'],
            ['volume', 'Volume'],
            ['percent', 'Income Percent'],
        ]
        factor = self.factor.create({
            'name': 'distance',
            'category': 'driver',
            'factor_type': 'distance',
            })
        for record in factor_type_list:
            factor.write({'factor_type': record[0]})
            factor._onchange_factor_type()
            self.assertEqual(factor.name, record[1], 'Onchange is not working')

    def test_20_get_amount_distance(self):
        factor = self.factor.create({
            'name': 'distance',
            'category': 'driver',
            'factor_type': 'distance',
            'factor': 2,
            })
        value = factor.get_amount(distance=100)
        self.assertEqual(value, 200, 'Error in factor calculation (distance)')

    def test_21_get_amount_distance_range(self):
        factor = self.factor.create({
            'name': 'distance',
            'category': 'driver',
            'factor_type': 'distance',
            'range_start': 0,
            'range_end': 1000,
            'factor': 2,
            })
        factor2 = self.factor.create({
            'name': 'distance',
            'category': 'driver',
            'factor_type': 'distance',
            'range_start': 1001,
            'range_end': 2000,
            'factor': 1,
            })
        factors = self.factor.browse([factor.id, factor2.id])
        value = factors.get_amount(distance=100)
        self.assertEqual(value, 200, 'Error in factor calculation (distance)')
        value = factors.get_amount(distance=1500)
        self.assertEqual(value, 1500, 'Error in factor calculation (distance)')

    def test_22_get_amount_distance_fixed_amount(self):
        factor = self.factor.create({
            'name': 'distance',
            'category': 'driver',
            'factor_type': 'distance',
            'factor': 2,
            'mixed': True,
            'fixed_amount': 100,
            })
        value = factor.get_amount(distance=100)
        self.assertEqual(value, 300, 'Error in factor calculation (distance)')

    def test_30_get_amount_distance_real(self):
        factor = self.factor.create({
            'name': 'distance_real',
            'category': 'driver',
            'factor_type': 'distance_real',
            'factor': 2,
            })
        value = factor.get_amount(distance_real=100)
        self.assertEqual(
            value, 200, 'Error in factor calculation (distance_real)')

    def test_31_get_amount_distance_real_range(self):
        factor = self.factor.create({
            'name': 'distance_real',
            'category': 'driver',
            'factor_type': 'distance_real',
            'range_start': 0,
            'range_end': 1000,
            'factor': 2,
            })
        factor2 = self.factor.create({
            'name': 'distance_real',
            'category': 'driver',
            'factor_type': 'distance_real',
            'range_start': 1001,
            'range_end': 2000,
            'factor': 1,
            })
        factors = self.factor.browse([factor.id, factor2.id])
        value = factors.get_amount(distance_real=100)
        self.assertEqual(
            value, 200, 'Error in factor calculation (distance_real)')
        value = factors.get_amount(distance_real=1500)
        self.assertEqual(
            value, 1500, 'Error in factor calculation (distance_real)')

    def test_32_get_amount_distance_real_fixed_amount(self):
        factor = self.factor.create({
            'name': 'distance_real',
            'category': 'driver',
            'factor_type': 'distance_real',
            'factor': 2,
            'mixed': True,
            'fixed_amount': 100,
            })
        value = factor.get_amount(distance_real=100)
        self.assertEqual(
            value, 300, 'Error in factor calculation (distance_real)')

    def test_40_get_amount_weight(self):
        factor = self.factor.create({
            'name': 'weight',
            'category': 'driver',
            'factor_type': 'weight',
            'factor': 2,
            })
        value = factor.get_amount(weight=100)
        self.assertEqual(
            value, 200, 'Error in factor calculation (weight)')

    def test_41_get_amount_weight_range(self):
        factor = self.factor.create({
            'name': 'weight',
            'category': 'driver',
            'factor_type': 'weight',
            'range_start': 0,
            'range_end': 1000,
            'factor': 2,
            })
        factor2 = self.factor.create({
            'name': 'weight',
            'category': 'driver',
            'factor_type': 'weight',
            'range_start': 1001,
            'range_end': 2000,
            'factor': 1,
            })
        factors = self.factor.browse([factor.id, factor2.id])
        value = factors.get_amount(weight=100)
        self.assertEqual(
            value, 200, 'Error in factor calculation (weight)')
        value = factors.get_amount(weight=1500)
        self.assertEqual(
            value, 1500, 'Error in factor calculation (weight)')

    def test_42_get_amount_weight_fixed_amount(self):
        factor = self.factor.create({
            'name': 'weight',
            'category': 'driver',
            'factor_type': 'weight',
            'factor': 2,
            'mixed': True,
            'fixed_amount': 100,
            })
        value = factor.get_amount(weight=100)
        self.assertEqual(
            value, 300, 'Error in factor calculation (weight)')

    def test_50_get_amount_travel(self):
        factor = self.factor.create({
            'name': 'travel',
            'category': 'driver',
            'factor_type': 'travel',
            'fixed_amount': 100,
            })
        value = factor.get_amount()
        self.assertEqual(
            value, 100, 'Error in factor calculation (travel)')

    def test_60_get_amount_qty(self):
        factor = self.factor.create({
            'name': 'qty',
            'category': 'driver',
            'factor_type': 'qty',
            'factor': 2,
            })
        value = factor.get_amount(qty=100)
        self.assertEqual(
            value, 200, 'Error in factor calculation (qty)')

    def test_61_get_amount_qty_range(self):
        factor = self.factor.create({
            'name': 'qty',
            'category': 'driver',
            'factor_type': 'qty',
            'range_start': 0,
            'range_end': 1000,
            'factor': 2,
            })
        factor2 = self.factor.create({
            'name': 'qty',
            'category': 'driver',
            'factor_type': 'qty',
            'range_start': 1001,
            'range_end': 2000,
            'factor': 1,
            })
        factors = self.factor.browse([factor.id, factor2.id])
        value = factors.get_amount(qty=100)
        self.assertEqual(
            value, 200, 'Error in factor calculation (qty)')
        value = factors.get_amount(qty=1500)
        self.assertEqual(
            value, 1500, 'Error in factor calculation (qty)')

    def test_62_get_amount_qty_fixed_amount(self):
        factor = self.factor.create({
            'name': 'qty',
            'category': 'driver',
            'factor_type': 'qty',
            'factor': 2,
            'mixed': True,
            'fixed_amount': 100,
            })
        value = factor.get_amount(qty=100)
        self.assertEqual(
            value, 300, 'Error in factor calculation (qty)')

    def test_70_get_amount_volume(self):
        factor = self.factor.create({
            'name': 'volume',
            'category': 'driver',
            'factor_type': 'volume',
            'factor': 2,
            })
        value = factor.get_amount(volume=100)
        self.assertEqual(
            value, 200, 'Error in factor calculation (volume)')

    def test_71_get_amount_volume_range(self):
        factor = self.factor.create({
            'name': 'volume',
            'category': 'driver',
            'factor_type': 'volume',
            'range_start': 0,
            'range_end': 1000,
            'factor': 2,
            })
        factor2 = self.factor.create({
            'name': 'volume',
            'category': 'driver',
            'factor_type': 'volume',
            'range_start': 1001,
            'range_end': 2000,
            'factor': 1,
            })
        factors = self.factor.browse([factor.id, factor2.id])
        value = factors.get_amount(volume=100)
        self.assertEqual(
            value, 200, 'Error in factor calculation (volume)')
        value = factors.get_amount(volume=1500)
        self.assertEqual(
            value, 1500, 'Error in factor calculation (volume)')

    def test_72_get_amount_volume_fixed_amount(self):
        factor = self.factor.create({
            'name': 'volume',
            'category': 'driver',
            'factor_type': 'volume',
            'factor': 2,
            'mixed': True,
            'fixed_amount': 100,
            })
        value = factor.get_amount(volume=100)
        self.assertEqual(
            value, 300, 'Error in factor calculation (volume)')

    def test_80_get_amount_percent(self):
        factor = self.factor.create({
            'name': 'percent',
            'category': 'driver',
            'factor_type': 'percent',
            'factor': 10,
            })
        value = factor.get_amount(income=1000)
        self.assertEqual(
            value, 100, 'Error in factor calculation (percent)')

    def test_81_get_amount_percent_fixed_amount(self):
        factor = self.factor.create({
            'name': 'percent',
            'category': 'driver',
            'factor_type': 'percent',
            'factor': 10,
            'mixed': True,
            'fixed_amount': 100,
            })
        value = factor.get_amount(income=1000)
        self.assertEqual(
            value, 200, 'Error in factor calculation (percent)')
