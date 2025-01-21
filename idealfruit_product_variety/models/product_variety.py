from odoo import models, fields


class ProductVariety(models.Model):
    _name = 'product.variety'
    _description = 'Product Variety'

    code = fields.Char(
        string='Code',
        required=True,
    )
    name = fields.Char(
        string='Name',
        required=True,
    )
    description = fields.Text(
        string='Description',
    )
    category_id = fields.Many2one(
        comodel_name='product.category',
        string='Categoría de Producto',
        help='Categoría a la que pertenece esta variedad.'
    )
