from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def print_control_mercancia_pdf(self, sale_orders):
        report = self.env.ref('idealfruit_custom_purchase.action_report_saleorder_mercancy_control')
        return report.report_action(sale_orders)

    def print_albaran_ventas_pdf(self, sale_orders):
        report = self.env.ref('idealfruit_custom_purchase.action_report_saleorder')
        return report.report_action(sale_orders)

    def print_cmr_pdf(self, sale_orders):
        report = self.env.ref('idealfruit_custom_purchase.action_report_saleorder_cmr')
        return report.report_action(sale_orders)

    def _get_shipping_address(self,is_company_id=False,partner=False):
        if not partner:
            return
        if is_company_id:
            partner = partner.partner_id
        shipping_addres_partner = partner.child_ids.filtered(lambda r: r.type == 'delivery')
        if shipping_addres_partner:
            return shipping_addres_partner[0]
        return partner


    def _get_fiscal_address(self,is_company_id=False, partner=False):
        if not partner:
            return
        if is_company_id:
            partner = partner.partner_id
        fiscal_address_partner = partner.child_ids.filtered(lambda r: r.type == 'invoice')
        if fiscal_address_partner:
            return fiscal_address_partner[0]
        return partner

    def _get_lines_to_cmr(self):
        purchase_order_line = self.env['purchase.order.line'].search([('sale_order_id', 'in', self.ids)],limit=1)
        resumen = {}
        if not purchase_order_line:
            return resumen
        purchase_order = purchase_order_line[0].order_id
        if not purchase_order:
            return resumen
        numero_de_palets = 0
        for line in purchase_order.order_line:
            if line.sale_order_id == self:
                product_id = line.product_id
                product_name=line.product_id.name
                numero_cajas = line.box
                if line.is_palet_base:
                    palets = 1
                else:
                    palets = 0
                numero_de_palets = numero_de_palets + palets
                peso = line.product_qty
                if product_id in resumen:
                    resumen[product_id]['numero_de_palets'] += numero_de_palets
                    resumen[product_id]['peso'] += peso
                    resumen[product_id]['numero_cajas'] += numero_cajas
                else:
                    resumen[product_id] = {
                        'product_name': product_name,
                        'numero_de_palets': numero_de_palets,
                        'peso': peso,
                        'numero_cajas': numero_cajas
                    }
        return resumen

    def _get_albaran_ventas_lines(self):
        purchase_order_line = self.env['purchase.order.line'].search([('sale_order_id', 'in', self.ids)], limit=1)
        if not purchase_order_line:
            return
        purchase_order = purchase_order_line[0].order_id
        if not purchase_order:
            return
        lines = []
        for line in purchase_order.order_line:
            if line.sale_order_id == self:
                lines.append(line)
        return lines


