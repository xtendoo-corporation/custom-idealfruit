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
