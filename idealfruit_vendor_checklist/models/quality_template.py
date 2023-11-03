# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models, api


class QualityTemplate(models.Model):
    _name = "quality.template"
    _description = "Plantilla de Calidad"

    name = fields.Char(
        string="Nombre",
        required=True,
    )
    quality_template_line_ids = fields.One2many(
        comodel_name="quality.template.line",
        inverse_name="quality_template_id",
        string="Líneas",
    )


