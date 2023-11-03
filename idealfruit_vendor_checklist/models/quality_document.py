# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class QualityDocument(models.Model):
    _name = "quality.document"
    _description = "Documentos de la plantilla de calidad"

    purchase_order_id = fields.Many2one(
        comodel_name="purchase.order",
        string="Pedido de compra",
    )
    quality_template_id = fields.Many2one(
        comodel_name="quality.template",
        string="Plantilla de calidad",
        required=True,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Producto",
    )
    res_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Productor",
    )
    quality_document_line_ids = fields.One2many(
        comodel_name="quality.document.line",
        inverse_name="quality_document_id",
        string="Líneas de documentos de calidad",
    )

    @api.onchange("quality_template_id")
    def _onchange_quality_template_id(self):
        for document in self:
            document.quality_document_line_ids = [(5, 0, 0)]
            for line in document.quality_template_id.quality_template_line_ids:
                document.quality_document_line_ids = [
                    (
                        0,
                        0,
                        {
                            "type": line.type,
                            "apellido": line.apellido,
                            "name": line.name,
                        },
                    )
                ]

            for line in document.quality_document_line_ids:
                print("="*80)
                print("line.name", line.name)
                print("line.type", line.type)
                print("line.apellido", line.apellido)
                print("="*80)
