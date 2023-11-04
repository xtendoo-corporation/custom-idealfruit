# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class QualityDocument(models.Model):
    _name = "quality.document"
    _description = "Documentos de la plantilla de calidad"

    purchase_order_id = fields.Many2one(
        comodel_name="purchase.order",
        string="Pedido de compra",
    )
    purchase_order_line_ids = fields.One2many(
        comodel_name="purchase.order.line",
        related="purchase_order_id.order_line",
        string="Líneas de pedido de compra",
    )
    quality_template_id = fields.Many2one(
        comodel_name="quality.template",
        string="Plantilla de calidad",
        required=True,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Producto",
        domain="[('id', 'in', allowed_product_ids)]",
    )
    allowed_product_ids = fields.Many2many(
        comodel_name="product.product",
        string="Allowed products",
        compute="_compute_allowed_product_ids",
    )
    res_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Productor",
        domain="[('id', 'in', allowed_partner_ids)]",
    )
    allowed_partner_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Allowed partners",
        compute="_compute_allowed_partners_ids",
    )
    quality_document_line_ids = fields.One2many(
        comodel_name="quality.document.line",
        inverse_name="quality_document_id",
        string="Líneas de documentos de calidad",
    )
    net_weight = fields.Float(
        string="Peso neto",
    )

    @api.depends("purchase_order_id.order_line")
    def _compute_allowed_product_ids(self):
        for quality_document in self:
            quality_document.allowed_product_ids = quality_document.purchase_order_id.order_line.mapped("product_id")

    @api.depends("purchase_order_id.order_line")
    def _compute_allowed_partners_ids(self):
        for quality_document in self:
            quality_document.allowed_partner_ids = quality_document.purchase_order_id.order_line.mapped("product_partner_id")

    @api.onchange("quality_template_id")
    def _onchange_quality_template_id(self):
        for document in self:
            document.quality_document_line_ids = [(5, 0, 0)]
            for line in document.quality_template_id.quality_template_line_ids:
                document.quality_document_line_ids = [
                    (0, 0, { "parameter_id": line.parameter_id})
                ]
