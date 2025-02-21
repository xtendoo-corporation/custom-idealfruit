from odoo import models, fields

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    palet_type_id = fields.Many2one('palet.type', string='Tipo de palet')
    is_palet_base = fields.Boolean('Palet Base', default=False)
