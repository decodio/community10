# -*- coding: utf-8 -*-
# Copyright 2016, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from psycopg2 import IntegrityError

from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


class TestTmsTransportable(TransactionCase):

    def setUp(self):
        super(TestTmsTransportable, self).setUp()
        self.transportable = self.env['tms.transportable']
        self.ton = self.env.ref('product.product_uom_ton')

    @mute_logger('openerp.sql_db')
    def test_10_tms_transportable_product_unique_name(self):
        with self.assertRaisesRegexp(
                IntegrityError,
                'duplicate key value violates unique constraint '
                '"tms_transportable_name_unique"'):
            self.transportable.create({'name': 'Test', 'uom_id': self.ton.id})
            self.transportable.create({'name': 'Test', 'uom_id': self.ton.id})
