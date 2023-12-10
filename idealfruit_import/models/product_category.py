# Copyright 2023 Manuel Calero <manuelcalero@xtendoo.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    default_code = fields.Char(
        string='Código',
    )
