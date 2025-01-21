from odoo import models, fields


class ProductCategory(models.Model):
    _inherit = 'product.category'

    product_variety_ids = fields.One2many(
        comodel_name='product.variety',
        inverse_name='category_id',
        string='Product Varieties',
        help='Varieties associated with this category.'
    )
