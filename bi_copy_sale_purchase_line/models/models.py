# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order.line'

    def copy_sale_order_line(self):
        self.copy(default={'order_id': self.order_id.id})


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def copy_purchase_order_line(self):
        new_purchase_line = self.copy(default={'order_id': self.order_id.id})
        #buscamos productores
        productors_to_add = self.env['purchase.line.productor'].search([('purchase_line_id', '=', self.id)])
        for productor in productors_to_add:
            values = productor.copy_data()[0]
            values['purchase_line_id'] = new_purchase_line.id
            self.env['purchase.line.productor'].create(values)
        #buscamos indicaciones
        indications_to_add = self.env['purchase.line.indications'].search([('purchase_line_id', '=', self.id)])
        for indication in indications_to_add:
            values = indication.copy_data()[0]
            values['purchase_line_id'] = new_purchase_line.id
            self.env['purchase.line.indications'].create(values)
