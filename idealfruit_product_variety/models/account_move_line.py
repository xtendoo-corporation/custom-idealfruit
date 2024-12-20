from odoo import models, fields

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

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
