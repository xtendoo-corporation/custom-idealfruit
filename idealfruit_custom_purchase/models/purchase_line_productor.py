from odoo import models, fields

class PurchaseLineProductor(models.Model):
    _name = 'purchase.line.productor'
    _description = 'Purchase Line Productor'

    purchase_line_id = fields.Many2one(
        'purchase.order.line', string='Purchase Order Line', required=True
    )
    related_partner_id = fields.Many2one(
        'res.partner', string='Proveedor', related='purchase_line_id.order_id.partner_id', store=True
    )
    partner_id = fields.Many2one(
        'res.partner', string='Productor', required=True,
    )
    product_variety_id = fields.Many2one(
        comodel_name='product.variety',
        string='Variedad de Producto'
    )

    product_variety_available_ids = fields.One2many(
        comodel_name='product.variety',
        inverse_name='category_id',
        string='Variedades Disponibles',
        related='purchase_line_id.product_id.categ_id.product_variety_ids',
        readonly=True
    )
    quantity = fields.Float(string='Cantidad', required=True)
    referencia_palet = fields.Char(string='Referencia Palet', required=True)


