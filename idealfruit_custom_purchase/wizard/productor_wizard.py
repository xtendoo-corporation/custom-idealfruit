# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ProductorWizard(models.Model):
    _name = 'productor.wizard'
    _description = 'Productor Wizard'

    order_id = fields.Many2one('purchase.order', string='Purchase Order', required=True)

    productor_line_ids = fields.One2many(
        'productor.wizard.line', 'wizard_id', string='Productor Lines'
    )

    def action_add_productor_lines(self):
        purchase_order_line = self.env['purchase.order.line'].browse(self._context.get('active_id'))
        wizard_id = self.env['productor.wizard'].create({
            'order_id': purchase_order_line.order_id.id,
        })
        quantity_to_add = 0
        for line in self.productor_line_ids:
            quantity_to_add = quantity_to_add + line.quantity
            self.env['productor.wizard.line'].create({
                'wizard_id': wizard_id.id,
                'partner_id': line.partner_id.id,
                'quantity': line.quantity,
                'referencia_palet': line.referencia_palet,
            })
        purchase_order_line.product_qty = quantity_to_add
        purchase_order_line.productor_wizard_id = wizard_id.id

class ProductorWizardLine(models.Model):
    _name = 'productor.wizard.line'
    _description = 'Productor Wizard Line'

    wizard_id = fields.Many2one('productor.wizard', string='Wizard Reference', required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Productor', required=True, domain="[('parent_id','=',partner_id),('type','=','productor')]",)
    quantity = fields.Float(string='Cantidad', required=True)
    referencia_palet = fields.Char(string='Referencia Palet', required=True)
