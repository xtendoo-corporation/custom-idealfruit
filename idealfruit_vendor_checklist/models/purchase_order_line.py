# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"


    product_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Productor",
        domain="[('parent_id','=',partner_id),('type','=','productor')]",
        required=True,
    )
    format_qty = fields.Float(
        string="Unidades formato",
        digits=(16,2),
    )
    format_id = fields.Many2one(
        comodel_name="idealfruit.format",
        string="Formato",
    )
