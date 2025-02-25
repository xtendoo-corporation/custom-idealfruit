# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class PurchaseOrderQualityDoc(models.Model):
    _name = "purchase.order.quality.doc"

    purchase_order_id = fields.Many2one(
        comodel_name="purchase.order",
        string="Orden de compra",
    )
    note = fields.Char(
        string="Nota",
    )
    attachment_ids = fields.One2many(
        comodel_name="ir.attachment",
        inverse_name="res_id",
        string="Adjuntos",
        tracking=True,
    )


