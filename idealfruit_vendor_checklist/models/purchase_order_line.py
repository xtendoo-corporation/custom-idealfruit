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
    box = fields.Float(
        string="Cajas",
        digits=(16, 2),
    )
    unit_box = fields.Float(
        string="Und. caja",
        digits=(16, 2),
        readonly=True,
    )
    visible_sequence = fields.Integer(
        "Número de palet",
        compute="_compute_visible_sequence",
        store=True,
    )

    @api.depends("sequence", "order_id.order_line")
    def _compute_visible_sequence(self):
        for so in self.mapped("order_id"):
            sequence = 1
            order_lines = so.order_line.filtered(lambda l: not l.display_type)
            for line in sorted(order_lines, key=lambda l: l.sequence):
                line.visible_sequence = sequence
                sequence += 1

    @api.onchange("product_id")
    def onchange_product(self):
        for record in self:
            record.unit_box = record.product_id.unit_box

    @api.onchange("box", "unit_box")
    def onchange_format(self):
        for record in self:
            record.product_qty = (record.box or 1) * (record.unit_box or 1)
