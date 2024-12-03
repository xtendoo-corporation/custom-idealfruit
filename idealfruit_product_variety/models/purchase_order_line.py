from odoo import models, fields

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_variety_id = fields.Many2one(
        comodel_name='product.variety',
        string='Product Variety'
    )

    def _prepare_account_move_line(self, move=False):
        res = super(PurchaseOrderLine, self)._prepare_account_move_line(move=move)
        res['product_variety_id'] = self.product_variety_id.id
        return res
