# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP,  Open Source Management Solution,  third party addon
#    Copyright (C) 2004-2017 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation,  either version 3 of the
#    License,  or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not,  see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models,  fields,  api,  _, http
from datetime import timedelta

from openerp.addons.mass_mailing.controllers.main import MassMailController
from openerp.http import request

import logging
_logger = logging.getLogger(__name__)

# https://www.privacy-regulation.eu
class MailMassMailingList(models.Model):
    _inherit = 'mail.mass_mailing.list'

    #consent_ids = fields.One2many(string='Recipients', comodel_name='gdpr.consent')
    gdpr_id = fields.Many2one(string='GDPR Inventory', comodel_name='gdpr.inventory')

class MailMassMailing(models.Model):
    _inherit = 'mail.mass_mailing'

    gdpr_id = fields.Many2one(string='GDPR Inventory', comodel_name='gdpr.inventory')
    gdpr_domain = fields.Text(string='GDPR Object IDs', compute='get_gdpr_domain')
    gdpr_consent = fields.Selection(selection=[('given', 'Given'), ('withdrawn', 'Withdrawn'), ('missing', 'Missing')], string='Consent State')
    gdpr_lawsection_consent = fields.Boolean(related='gdpr_id.lawsection_id.consent')
    recipients = fields.Integer(readonly=True)
    gdpr_mailing_list_ids = fields.Many2many(comodel_name='gdpr.mail.mass_mailing.list', string='GDPR Mailing Lists')
    gdpr_consent_collected = fields.Many2many(string='Collected GDPR Inventory', comodel_name='gdpr.inventory')

    @api.onchange('gdpr_id', 'gdpr_consent')
    def get_gdpr_domain(self):
        domain = []
        if self.gdpr_id:
            if self.gdpr_id.lawsection_id.consent:
                if self.gdpr_consent in ['given', 'withdrawn']:
                    object_ids = [d['gdpr_object_id'][0] for d in self.env['gdpr.consent'].search_read([('state', '=', self.gdpr_consent), ('gdpr_id', '=', self.gdpr_id.id)], ['gdpr_object_id'])]
                else:
                    object_ids = (self.gdpr_id.object_ids - self.env['gdpr.consent'].search([('gdpr_id', '=', self.gdpr_id.id)]).mapped('gdpr_object_id')).mapped('id')
                # ~ _logger.warn(self.env['gdpr.object'].search_read([('id', 'in', object_ids), ('restricted', '=', False)], ['object_res_id']))
                # ~ object_ids = [d['object_res_id'] for d in self.env['gdpr.object'].search_read([('id', 'in', object_ids), ('restricted', '=', False)], ['object_res_id'])]
            else:
                object_ids = [d['object_res_id'] for d in self.env['gdpr.object'].search_read([('gdpr_id', '=', self.gdpr_id.id), ('restricted', '=', False)], ['object_res_id'])]
            domain = [('id', 'in', object_ids)]
            self.recipients = len(object_ids)
        self.gdpr_domain = domain

    @api.onchange('mailing_model', 'gdpr_mailing_list_ids')
    def on_change_gdpr_model_and_list(self):
        consents = set()
        partners = set()
        for lst in self.gdpr_mailing_list_ids:
            for consent_ids in lst.mapped('gdpr_ids').mapped('consent_ids'):
                con = consent_ids.filtered(lambda c: c.state == lst.gdpr_consent and c.partner_id.id not in partners)
                partners = partners.union(set(con.mapped('partner_id').mapped('id')))
                consents = consents.union(set(con.mapped('id')))
        self.mailing_domain = "[('id', 'in', %s)]" %list(consents)

    @api.model
    def get_recipients(self, mailing):
        if mailing.mailing_model == 'gdpr.consent':
            consents = set()
            partners = set()
            for lst in mailing.gdpr_mailing_list_ids:
                for consent_ids in lst.mapped('gdpr_ids').mapped('consent_ids'):
                     con = consent_ids.filtered(lambda c: c.state == lst.gdpr_consent and c.partner_id.id not in partners)
                partners = partners.union(set(con.mapped('partner_id').mapped('id')))
                consents = consents.union(set(con.mapped('id')))
            return consents
        else:
            return super(MailMassMailing, self).get_recipients(mailing)


class GDPRMailMassMailingList(models.Model):
    _name = 'gdpr.mail.mass_mailing.list'

    name = fields.Char(string='name', required=True)
    gdpr_ids = fields.Many2many(comodel_name='gdpr.inventory', string='GDPRs')
    gdpr_consent = fields.Selection(selection=[('given', 'Given'), ('withdrawn', 'Withdrawn'), ('missing', 'Missing')], string='Consent State')
    consent_nbr = fields.Integer(compute='_get_consent_nbr', string='Number of Contacts')

    @api.one
    def _get_consent_nbr(self):
        self.consent_nbr = len(self.env['gdpr.consent'].search([('gdpr_id', 'in', self.gdpr_ids.mapped('id'))]))

    @api.model
    def get_consents(self, mailing):
        consents = self.env['gdpr.consent'].browse()
        # TODO: handle missing consents
        for inventory in mailing.gdpr_ids:
            consents |= inventory.consent_ids.filtered(lambda c: c.state == mailing.gdpr_consent)
        return consents

    @api.one
    def create_missing_consents(self):
        for inventory in self.gdpr_ids:
            for partner in inventory.partner_ids:
                if not partner.consent_ids.filtered(lambda c: c.gdpr_id == inventory):
                    self.env['gdpr.consent'].create({
                        'name': '%s - %s' %(inventory.name, partner.name),
                        'record_id': '%s,%s' %(partner._name, partner.id),
                        'partner_id': partner.id,
                        'gdpr_id': inventory.id,
                        'state': self.gdpr_consent,
                    })


class gdpr_consent(models.Model):
    _inherit = 'gdpr.consent'

    _mail_mass_mailing = _('GDPR Consents')


class MassMailController(MassMailController):

    @http.route(['/mail/mailing/<int:mailing_id>/unsubscribe'], type='http', auth='none', website=True)
    def mailing(self, mailing_id, email=None, res_id=None, **post):
        res = super(MassMailController, self).mailing(mailing_id, email, res_id, **post)
        if res.get_data() == 'OK':
            mailing = request.env['mail.mass_mailing'].sudo().browse(mailing_id)
            if mailing.mailing_model == 'mail.mass_mailing.contact':
                list_ids = [l.id for l in mailing.contact_list_ids]
                records = request.env[mailing.mailing_model].sudo().search([('list_id', 'in', list_ids), ('id', '=', res_id), ('email', 'ilike', email)])
                consent = request.env['gdpr.consent'].sudo().search([('gdpr_object_id.record_id', '=', '%s,%s' % (mailing.mailing_model, records.id))])
                if consent:
                    consent.remove("User unsubscribed through %s (referer: %s)" % (request.httprequest.path, request.httprequest.referrer))
            elif mailing.gdpr_id and res_id:
                consent = request.env['gdpr.consent'].sudo().search([
                    ('record_id', '=', '%s,%s' % (mailing.mailing_model, res_id)),
                    ('partner_id.email', '=', email),
                    ('gdpr_id', '=', mailing.gdpr_id.id)])
                if consent:
                    consent.remove("User unsubscribed through %s (referer: %s)" % (request.httprequest.path, request.httprequest.referrer))
        return res

    @http.route(['/mail/consent/<int:mailing_id>/partner/<int:partner_id>'], type='http', auth='none', website=True)
    def mailing_consents(self, mailing_id, partner_id, **post):
        mailing = request.env['mail.mass_mailing'].sudo().browse(mailing_id)
        partner = request.env['res.partner'].sudo().browse(partner_id)
        if mailing and partner:
            return request.website.render('gdpr_mass_mailing.mailing_consents', {'mailing': mailing, 'partner': partner})
