# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class PurchaseOrderQualityDoc(models.Model):
    _name = "purchase.order.quality.doc"

    purchase_order_id = fields.Many2one(
        comodel_name="purchase.order",
        string="Orden de compra",
    )
    url = fields.Char(
        string="Enlace",
    )

    @api.model
    def action_purchase_order_quality_doc(self, vals):
        for record in self:
            print("*"*80)
            print("record", record.url)

        for val in vals:
            print("*"*80)
            print("val", val)

        print("action_purchase_order_quality_doc****************")
        print("url", self.url)
        print("vals", vals)

        return {
            'type': 'ir.actions.act_url',
            'url': self.url,
            'target': 'new',
        }
