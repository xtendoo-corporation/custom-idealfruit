# Copyright 2023 Manuel Calero <manuelcalero@xtendoo.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class IdealFruitFormat(models.Model):
    _name = 'idealfruit.format'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Ideal Fruit Format"

    name = fields.Char(
        string="Nombre",
        required=True,
    )
    alfinf_id = fields.Float(
        string="Alfinf id",
    )
    format = fields.Float(
        string="Unidades en formato",
    )
    units = fields.Integer(
        string="Número de unidades en caja",
    )
    pieces = fields.Integer(
        string="Número de piezas",
    )
    quality_category = fields.Integer(
        string="Categoría de calidad",
    )
    container_field = fields.Float(
        string="Contenedor",
    )
    container_sale = fields.Float(
        string="Contenedor venta",
    )
    kg_cost = fields.Float(
        string="Costo por kilo",
    )
    # Granel
    bulk = fields.Boolean(
        string="Granel",
    )
    input_output = fields.Selection(
        selection=[
            ("input", "Entrada"),
            ("output", "Salida"),
            ("both", "Entrada y Salida"),
        ],
        string="Uso del formato",
        default="both",
    )


