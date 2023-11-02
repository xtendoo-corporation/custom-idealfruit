# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class TemplateQualityDocumentRelation(models.Model):
    _name = "template.quality.document.relation"
    _description = "Relación de documentos de la plantilla de calidad"

    template_quality_document_id = fields.Many2one(
        comodel_name="template.quality.document",
        string="Documento",
    )
    name = fields.Char(
        string="Nombre",
        required=True,
    )
    type = fields.Selection(
        selection=[
            ("text", "Texto"),
            ("percentage", "Porcentaje"),
            ("float", "Númerico"),
            ("boolean", "Presente/Ausente"),
            ("date", "Fecha"),
            ("datetime", "Fecha y Hora"),
        ],
        string="Tipo de Campo",
        required=True,
    )
    text_value = fields.Char(
        string="Valor Texto",
    )
    percentage_value = fields.Float(
        string="Valor Porcentaje",
    )
    numeric_value = fields.Float(
        string="Valor Númerico",
    )
    boolean_value = fields.Boolean(
        string="Valor Booleano",
    )
    date_value = fields.Date(
        string="Valor Fecha",
    )
    datetime_value = fields.Datetime(
        string="Valor Fecha y Hora",
    )
    result_value = fields.Char(
        string="Valor",
        compute="_compute_result_value",
        store=True,
    )

    @api.depends("type", "text_value", "percentage_value", "numeric_value", "boolean_value", "date_value", "datetime_value")
    def _compute_result_value(self):
        for record in self:
            if record.type == "text":
                record.result_value = record.text_value
            elif record.type == "percentage":
                record.result_value = str(record.percentage_value) + "%"
            elif record.type== "float":
                record.result_value = str(record.numeric_value)
            elif record.type== "boolean":
                record.result_value = "Presente" if record.boolean_value else "Ausente"
            elif record.type== "date":
                record.result_value = str(record.date_value)
            elif record.type== "datetime":
                record.result_value = str(record.datetime_value)
            else:
                record.result_value = ""
