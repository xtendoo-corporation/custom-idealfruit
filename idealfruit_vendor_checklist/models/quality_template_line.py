# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models, api


class TemplateQualityLine(models.Model):
    _name = "quality.template.line"
    _description = "Líneas de plantilla de calidad"

    quality_template_id = fields.Many2one(
        comodel_name="quality.template",
        string="Plantilla de Calidad",
    )
    parameter_id = fields.Many2one(
        comodel_name="quality.parameter",
        string="Parámetro",
        required=True,
    )
    parameter_type = fields.Selection(
        related="parameter_id.type",
        string="Tipo",
    )
