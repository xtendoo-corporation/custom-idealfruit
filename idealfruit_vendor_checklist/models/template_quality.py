# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models, api


class TemplateQuality(models.Model):
    _name = "template.quality"
    _description = "Template Quality"

    name = fields.Char(
        string="Nombre",
        required=True,
    )
    template_quality_line_ids = fields.One2many(
        comodel_name="template.quality.line",
        inverse_name="template_quality_id",
        string="Lineas",
    )


