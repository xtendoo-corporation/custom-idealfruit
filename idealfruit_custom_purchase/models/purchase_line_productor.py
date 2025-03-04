from odoo import models, fields, api

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
    # box_order = fields.Float(
    #     string="Cajas Pedidas",
    #     digits=(16, 2),
    #     related='purchase_line_id.box',
    # )
    box = fields.Float(
        string="Cajas Entregadas",
        digits=(16, 2),
    )
    unit_box = fields.Float(
        string="Und. caja",
        digits=(16, 2),
        readonly=True,
        related='purchase_line_id.unit_box',
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
    quantity = fields.Float(string='kilos entregados', readonly=True, store=True)
    # quantity_order = fields.Float(string='kilos Pedidos', required=True,  related='purchase_line_id.product_qty')
    referencia_palet = fields.Char(string='Referencia Palet')

    @api.onchange("box", "unit_box")
    def onchange_format(self):
        for record in self:
            record.quantity = record.box * record.unit_box


