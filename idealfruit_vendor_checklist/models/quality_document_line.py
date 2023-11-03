# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class QualityDocumentLine(models.Model):
    _name = "quality.document.line"
    _description = "Líneas de documentos de calidad"

    quality_document_id = fields.Many2one(
        comodel_name="quality.document",
        string="Documento",
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
    value = fields.Float(
        string="Valor",
    )
    text = fields.Char(
        string="Texto",
        compute="_compute_text",
    )

    @api.depends("type", "value")
    def _compute_result(self):
        for record in self:
            if record.type == "peso":
                record.text = str(record.value) + "(gr)"
            elif record.type== "unidad":
                record.text = str(record.value) + "(ud)"
            else:
                record.text = ""






