# -*- coding: utf-8 -*-
# Copyright 2016, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
import os
from codecs import BOM_UTF8
from datetime import datetime

from lxml import objectify
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class TmsExpenseLine(models.Model):
    _inherit = 'tms.expense.line'

    xml_file = fields.Binary(attachment=True)
    xml_filename = fields.Char()
    pdf_file = fields.Binary(attachment=True)
    pdf_filename = fields.Char()

    @api.onchange('xml_file')
    def _onchange_xml_file(self):
        if self.xml_file:
            xml_extension = os.path.splitext(self.xml_filename)[1].lower()
            if xml_extension != '.xml':
                raise ValidationError(_(
                    'Verify that file be .xml, please!'))
            xml_str = base64.decodestring(self.xml_file).lstrip(BOM_UTF8)
            xml = objectify.fromstring(xml_str)
            xml_vat_emitter = xml.Emisor.get('rfc', '')
            xml_name_emitter = xml.Emisor.get('nombre', '')
            xml_folio = xml.get('folio', '')
            xml_date = xml.get('fecha', '')

            partner_id = self.env['res.partner'].search(
                ['|', ('vat', '=', 'MX' + xml_vat_emitter),
                 ('name', '=ilike', xml_name_emitter)], limit=1)
            date_split = xml_date.split('T')
            strp_date = datetime.strptime(date_split[0], '%Y-%m-%d')

            self.invoice_number = xml_folio
            self.date = strp_date
            if not partner_id:
                raise ValidationError(
                    _('The supplier %s dont exist in the system'
                        'please check de supplier list.') %
                    xml_name_emitter)
            self.partner_id = partner_id.id
        else:
            self.invoice_number = False
            self.date = False
            self.partner_id = False
