# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class QualityDocumentLine(models.Model):
    _name = "quality.document.line"
    _description = "Líneas de documentos de calidad"

    quality_document_id = fields.Many2one(
        comodel_name="quality.document",
        string="Documento",
    )
    net_weight = fields.Float(
        string="Peso neto",
        related="quality_document_id.net_weight",
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
    value = fields.Float(
        string="Valor",
    )
    percentage = fields.Float(
        string="Porcentaje %",
        compute="_compute_percentage",
    )

    @api.depends("parameter_type", "value", "net_weight")
    def _compute_percentage(self):
        for record in self:
            if record.net_weight == 0:
                record.percentage = 0
            elif record.parameter_type == "porcentaje":
                record.percentage = record.value / record.net_weight * 100
            else:
                record.percentage = record.value

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
        compute="_compute_result",
    )

    @api.depends("parameter_id", "value")
    def _compute_result(self):
        for record in self:
            if record.parameter_id.type == "unidad":
                record.result = record.parameter_id.quality_parameter_line_ids.filtered(
                    lambda x: x.result == str(int(record.value))
                ).result or "6"
            else:
                record.result = record.parameter_id.quality_parameter_line_ids.filtered(
                    lambda x: x.greater_than < record.percentage <= x.less_than
                ).result or "6"
