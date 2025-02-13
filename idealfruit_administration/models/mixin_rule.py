# Copyright 2023 Xtendoo (https://xtendoo.es)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).from odoo import api, models, fields
from odoo import api, models, fields, _


class MixinRule(models.Model):
    _name = 'mixin.rule'
    _description = 'Mixin rule'

    def _get_default_not_create_group(self):
        return self.env["res.users"].has_group(
            "idealfruit_administration.group_not_create"
        )

    def _is_not_create_group(self):
        self.is_admin = self.env["res.users"].has_group(
            "idealfruit_administration.group_not_create"
        )

    not_create_group = fields.Boolean(
        compute='_is_not_create_group',
        string="NotCreateGroup",
        default=lambda self: self._get_default_not_create_group()
    )
