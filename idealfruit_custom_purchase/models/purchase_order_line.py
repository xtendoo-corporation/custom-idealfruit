from odoo import models, fields, api, _

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    palet_type_id = fields.Many2one('palet.type', string='Tipo de palet')
    is_palet_base = fields.Boolean('Palet Base', default=True)
    base_palet_line_id = fields.Many2one(
        'purchase.order.line',
        string='Linea Base',
        domain="[('id', 'in', base_palet_line_ids)]"
    )
    base_palet_line_id_number = fields.Integer(
        "Número de palet base",
        related="base_palet_line_id.visible_sequence",
    )
    base_palet_line_ids = fields.Many2many(
        'purchase.order.line',
        compute='_compute_base_palet_line_ids',
        string='Base Palet Lines'
    )

    productor_ids = fields.One2many(
        'purchase.line.productor', 'purchase_line_id', string='Productores'
    )
    indications_ids = fields.One2many(
        'purchase.line.indications', 'purchase_line_id', string='Indicaciones'
    )
    qty_delivered = fields.Float(string='Cantidad Entregada',store=True)

    @api.onchange('order_id', 'is_palet_base')
    def _compute_base_palet_line_ids(self):
        for line in self:
            if line.is_palet_base:
                line.base_palet_line_id = False
            if line.order_id:
                line.base_palet_line_ids = line.order_id.order_line.filtered(lambda l: l.is_palet_base)
            else:
                line.base_palet_line_ids = self.env['purchase.order.line']

    def action_abrir_productor_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Productores para la línea %s-%s' % (self.visible_sequence, self.name)),
            'res_model': 'purchase.order.line',
            'res_id': self.id,
            'view_mode': 'form',
            'view_id': self.env.ref('idealfruit_custom_purchase.view_purchase_line_productor_update').id,
            'target': 'new',
        }

    def action_guardar_y_procesar(self):
        qty_to_update = 0.00
        for record in self:
            productor_line_ids =self.env['purchase.line.productor'].search([('purchase_line_id', '=', record.id)])
            for productor in productor_line_ids:
                qty_to_update += productor.quantity
            record.qty_delivered = qty_to_update

        return {'type': 'ir.actions.act_window_close'}

    def action_abrir_indications_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Indicaciones para la línea %s-%s' % (self.visible_sequence, self.name)),
            'res_model': 'purchase.order.line',
            'res_id': self.id,
            'view_mode': 'form',
            'view_id': self.env.ref('idealfruit_custom_purchase.view_purchase_line_indications_update').id,
            'target': 'new',
        }

