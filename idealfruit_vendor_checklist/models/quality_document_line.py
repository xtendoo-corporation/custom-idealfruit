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
    firmness_units = fields.Float(
        string="Unidades de firmeza",
        related="quality_document_id.firmness_units",
    )
    appearance_units = fields.Float(
        string="Unidades de apariencia",
        related="quality_document_id.appearance_units",
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


    @api.depends("parameter_type", "value", "net_weight", "firmness_units", "appearance_units")
    def _compute_percentage(self):
        for record in self:
            record.percentage = 0
            if record.parameter_type == "unidad":
                record.percentage = record.value
            if record.parameter_type == "apariencia" and record.appearance_units > 0:
                record.percentage = record.value / ( record.appearance_units / 10 )
            elif record.parameter_type == "porcentaje" and record.net_weight > 0:
                record.percentage = record.value / record.net_weight * 100
            elif record.parameter_type == "firmeza" and record.firmness_units > 0:
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

    @api.depends("parameter_id", "percentage")
    def _compute_result(self):
        for record in self:
            if record.parameter_id.type == "unidad":
                record.result = record.parameter_id.quality_parameter_line_ids.filtered(
                    lambda x: x.result == str(int(record.value))
                ).result or "6"
            else:

                print("*"*80)
                print("record.percentage", record.percentage)
                print("record.parameter_id.quality_parameter_line_ids",
                      record.parameter_id.quality_parameter_line_ids.filtered(lambda x: x.greater_than < record.percentage <= x.less_than))
                print("*"*80)

                record.result = record.parameter_id.quality_parameter_line_ids.filtered(
                    lambda x: x.greater_than < record.percentage <= x.less_than
                ).result or "6"
