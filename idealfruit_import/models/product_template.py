# Copyright 2023 Manuel Calero <manuelcalero@xtendoo.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProuctTemplate(models.Model):
    _inherit = 'product.template'

    is_bulk = fields.Boolean(
        string='A granel',
    )
    unit_box = fields.Integer(
        string='Unidades por caja',
    )
    is_ecological = fields.Boolean(
        string='Ecológico',
    )
