#!/usr/bin/python
# -*- coding: utf8 -*-

from odoo.addons.report_aeroo.ctt_objects import ctt_currency


class eur(ctt_currency):

    def _init_currency(self):
        self.language = u'de_DE'
        self.code = u'EUR'
        self.fractions = 100
        self.cur_singular = u' euro'
        self.cur_plural = u' euro'
        self.frc_singular = u' cent'
        self.frc_plural = u' cents'
        # grammatical genders: f - feminine, m - masculine, n -neuter
        self.cur_gram_gender = 'm'
        self.frc_gram_gender = 'm'

eur()
