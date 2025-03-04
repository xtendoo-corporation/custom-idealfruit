from odoo import models, fields

class PurchaseLineIndications(models.Model):
    _name = 'purchase.line.indications'
    _description = 'Purchase Line Indications'

    purchase_line_id = fields.Many2one(
        'purchase.order.line', string='Purchase Order Line', required=True
    )
    indications = fields.Text(string='Indicaciones')
    indications_attachment = fields.Binary(string='Adjunto')


