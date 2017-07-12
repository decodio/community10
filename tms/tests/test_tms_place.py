# -*- coding: utf-8 -*-
# Copyright 2016, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from mock import MagicMock
from odoo import api
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestTmsPlace(TransactionCase):

    def setUp(self):
        super(TestTmsPlace, self).setUp()
        self.place = self.env.ref('tms.tms_place_01')

    def test_10_tms_place_get_coordinates(self):
        self.place.get_coordinates()
        self.assertEqual(self.place.latitude, float('29.4241219000'),
                         'Latitude is done')
        self.assertEqual(self.place.longitude, float('-98.4936282000'),
                         'Longitude is working')

    def test_20_tms_place_open_in_google(self):
        self.place.open_in_google()

    def test_30_tms_place_compute_complete_name(self):
        self.place._compute_complete_name()
        self.assertEqual(self.place.complete_name, 'San Antonio, Texas',
                         'Full Complete Name')

    @api.depends('name', 'state_id')
    def test_40_tms_place_compute_complete_name(self):
        self.place.write({'name': 'San Francisco'})
        self.place._compute_complete_name()
        self.assertEqual(
            self.place.complete_name,
            'San Francisco, Texas',
            'On change works')
        self.place.write({'state_id': False})
        self.place._compute_complete_name()
        self.assertEqual(
            self.place.complete_name,
            'San Francisco',
            'On change works')

    def test_50_tms_place_get_cordinates(self):
        self.place.get_coordinates = MagicMock()
        attrs = {'other.side_effect': UserError}
        self.place.get_coordinates.configure_mock(**attrs)
        self.place.get_coordinates.other()
