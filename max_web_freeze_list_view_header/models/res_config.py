from odoo import models, fields, api


class BaseConfigSettings(models.TransientModel):
    _inherit = 'base.config.settings'

    use_freeze_on_forms = fields.Boolean('Use header freeze on forms?', default=False)

    def set_use_freeze_on_forms(self):
        res = self.env['ir.values'].sudo().set_default('base.config.settings', 'use_freeze_on_forms',
                                                       self.use_freeze_on_forms)
        return res

    def get_use_freeze_on_forms(self):
        return self.env['ir.values'].get_default('base.config.settings', 'use_freeze_on_forms')