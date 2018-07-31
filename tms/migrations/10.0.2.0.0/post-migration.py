# -*- coding: utf-8 -*-
import logging

from odoo import SUPERUSER_ID, api
_logger = logging.getLogger(__name__)


def remove_base_geoengine(cr):

    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        module = env.ref('base.module_base_geoengine')
        module.button_uninstall()


def migrate(cr, version):
    if not version:
        return
    remove_base_geoengine(cr)
