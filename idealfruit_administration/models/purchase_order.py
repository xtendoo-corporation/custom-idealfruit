from odoo import models, api, fields

class PurchaseOrder(models.Model):
    _inherit = ['purchase.order', 'mixin.rule']
    _name="purchase.order"

class PurchaseOrderLine(models.Model):
    _inherit = ['purchase.order.line', 'mixin.rule']
    _name = "purchase.order.line"

