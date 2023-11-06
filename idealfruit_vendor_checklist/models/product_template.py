# Copyright 2023 Manuel Calero <manuelcalero@xtendoo.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    quality_template_id = fields.Many2one(
        comodel_name="quality.template",
        string="Plantilla de Calidad",
    )
