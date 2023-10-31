# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models, api


class TemplateQualityLine(models.Model):
    _name = "template.quality.line"
    _description = "Template Quality Line"

    template_quality_id = fields.Many2one(
        comodel_name="template.quality",
        string="Template Quality",
    )
    name = fields.Char(
        string="Nombre",
        required=True,
    )
    field_type = fields.Selection(
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
    field_value = fields.Char(
        string="Valor",
        compute="_compute_field_type_value",
        store=True,
    )

    @api.depends("field_type", "text_value", "percentage_value", "numeric_value", "boolean_value", "date_value", "datetime_value")
    def _compute_field_type_value(self):
        for record in self:
            if record.field_type == "text":
                record.field_value = record.text_value
            elif record.field_type == "percentage":
                record.field_value = str(record.percentage_value) + "%"
            elif record.field_type == "float":
                record.field_value = str(record.numeric_value)
            elif record.field_type == "boolean":
                record.field_value = "Presente" if record.boolean_value else "Ausente"
            elif record.field_type == "date":
                record.field_value = str(record.date_value)
            elif record.field_type == "datetime":
                record.field_value = str(record.datetime_value)
            else:
                record.field_value = ""

