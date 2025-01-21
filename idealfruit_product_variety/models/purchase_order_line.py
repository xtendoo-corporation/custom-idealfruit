from odoo import models, fields


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_variety_id = fields.Many2one(
        comodel_name='product.variety',
        string='Variedad de Producto'
    )

    product_variety_available_ids = fields.One2many(
        comodel_name='product.variety',
        inverse_name='category_id',
        string='Variedades Disponibles',
        related='product_id.categ_id.product_variety_ids',
        readonly=True
    )

    def _prepare_account_move_line(self, move=False):
        res = super(PurchaseOrderLine, self)._prepare_account_move_line(move=move)
        res['product_variety_id'] = self.product_variety_id.id
        return res
