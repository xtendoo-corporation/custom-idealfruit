from odoo import models, fields

class PurchaseLineProductor(models.Model):
    _name = 'purchase.line.productor'
    _description = 'Purchase Line Productor'

    purchase_line_id = fields.Many2one(
        'purchase.order.line', string='Purchase Order Line', required=True
    )
    partner_id = fields.Many2one(
        'res.partner', string='Productor', required=True,
        domain="[('parent_id','=',partner_id),('type','=','productor')]"
    )
    quantity = fields.Float(string='Cantidad', required=True)
    referencia_palet = fields.Char(string='Referencia Palet', required=True)


