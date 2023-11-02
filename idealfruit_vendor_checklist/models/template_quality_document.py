# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class TemplateQualityDocument(models.Model):
    _name = "template.quality.document"
    _description = "Documentos de la plantilla de calidad"

    purchase_order_id = fields.Many2one(
        comodel_name="purchase.order",
        string="Pedido de compra",
    )
    template_quality_id = fields.Many2one(
        comodel_name="template.quality",
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
    template_quality_document_relation_ids = fields.One2many(
        comodel_name="template.quality.document.relation",
        inverse_name="template_quality_document_id",
        string="Valores de documentos de calidad",
    )

    @api.onchange("template_quality_id")
    def _on_change_template_quality_id(self):
        for template_quality_document in self:
            template_quality_document.template_quality_document_relation_ids = [
                (5, 0, 0)
            ]
            for document in template_quality_document.template_quality_id.template_quality_line_ids:
                print("*"*80)
                print("name", document.name)
                print("type", document.type)
                print("text_value", document.text_value)
                print("*"*80)
                template_quality_document.template_quality_document_relation_ids = [
                    (
                        0,
                        0,
                        {
                            "name": document.name,
                            "text_value": document.text_value,
                            "percentage_value": document.percentage_value,
                            "numeric_value": document.numeric_value,
                            "boolean_value": document.boolean_value,
                            "date_value": document.date_value,
                            "datetime_value": document.datetime_value,
                        },
                    )
                ]


                # "type": document.type,
