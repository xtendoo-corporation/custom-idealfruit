# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models, api


class QualityParameter(models.Model):
    _name = "quality.parameter"
    _description = "Parámetros de Calidad"

    name = fields.Char(
        string="Nombre",
        required=True,
    )
    type = fields.Selection(
        selection=[
            ("unidad", "Unidad"),
            ("porcentaje", "Porcentaje"),
            ("firmeza", "Firmeza"),
            ("apariencia", "Apariencia"),
        ],
        string="Tipo",
        required=True,
    )
    quality_parameter_type_id = fields.Many2one(
        comodel_name="quality.parameter.type",
        string="Tipo de parámetro",
        required=True,
    )
    quality_parameter_qualify_id = fields.Many2one(
        comodel_name="quality.parameter.qualify",
        string="Calificación",
        required=True,
    )
    quality_parameter_line_ids = fields.One2many(
        comodel_name="quality.parameter.line",
        inverse_name="quality_parameter_id",
        string="Líneas",
    )


