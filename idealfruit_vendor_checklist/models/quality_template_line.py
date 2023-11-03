# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models, api


class TemplateQualityLine(models.Model):
    _name = "quality.template.line"
    _description = "Líneas de plantilla de calidad"

    quality_template_id = fields.Many2one(
        comodel_name="quality.template",
        string="Plantilla de Calidad",
    )
    name = fields.Char(
        string="Nombre",
        required=True,
    )
    apellido = fields.Char(
        string="Apellido",
    )
    type = fields.Selection(
        selection=[
            ("peso", "Peso en gr"),
            ("unidad", "Unidad"),
        ],
        string="Tipo",
        required=True,
    )
