# -*- coding: utf-8 -*-
# Copyright 2016, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestTmsRoute(TransactionCase):

    def setUp(self):
        super(TestTmsRoute, self).setUp()
        self.route = self.env.ref('tms.tms_route_01')
        self.vehicle = self.env.ref('tms.tms_fleet_vehicle_01')

    def test_10_tms_route_on_change_distance_empty(self):
        self.route.write({'distance_empty': 150.00})
        self.route.on_change_disance_empty()
        self.assertEqual(
            self.route.distance_loaded,
            737.00,
            'On change works')

    def test_20_tms_route_on_change_distance_loaded(self):
        self.route.write({'distance_loaded': 150.00})
        self.route.on_change_disance_loaded()
        self.assertEqual(
            self.route.distance_empty,
            737.00,
            'On change works')

    def test_30_tms_route_get_route_info(self):
        self.route.get_route_info()
        self.assertGreater(self.route.travel_time, 0,
                           msg='Travel time is not correct')
        self.assertGreater(self.route.distance, 0,
                           msg='Distance is not correct')

    def test_40_tms_route_open_in_google(self):
        self.route.open_in_google()

    def test_50_tms_route_get_fuel_efficiency(self):
        self.route.get_fuel_efficiency(self.vehicle, 'double')
