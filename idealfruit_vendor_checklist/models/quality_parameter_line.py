# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models, api


class QualityParameterLine(models.Model):
    _name = "quality.parameter.line"
    _description = "Lineas de Parámetros de Calidad"

    quality_parameter_id = fields.Many2one(
        comodel_name="quality.parameter",
        string="Parámetro",
        required=True,
    )
    parameter_type = fields.Selection(
        related="quality_parameter_id.type",
        string="Tipo",
    )
    result = fields.Selection(
        selection=[
            ("1", "Excelente (1)"),
            ("2", "Bueno (2)"),
            ("3", "Aceptable (3)"),
            ("4", "Menos que la media (4)"),
            ("5", "Pobre (5)"),
            ("6", "Perdida total (6)"),
        ],
        string="Resultado",
        required=True,
    )
    greater_than = fields.Float(
        string="Mayor que",
    )
    less_than = fields.Float(
        string="Menor o igual que",
    )
    sequence = fields.Integer(
        default=10,
    )

    _sql_constraints = [
        (
            "unique_parameter",
            "UNIQUE(quality_parameter_id, result)",
            "No puede haber dos resultados iguales para el mismo parámetro",
        ),
        (
            "greater_than_less_than",
            "CHECK(greater_than <= less_than)",
            "El valor 'Mayor que' debe ser menor que el valor 'Menor o igual que'",
        ),
    ]


