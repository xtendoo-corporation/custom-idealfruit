
from odoo import models, fields, api
from odoo.exceptions import UserError
import base64

import logging  # Esto es necesario para usar los log

_logger = logging.getLogger(__name__)


class SelectSalesWizard(models.TransientModel):
    _name = 'select.sales.wizard'
    _description = 'Seleccionar Órdenes de Venta'

    sale_order_ids = fields.Many2many('sale.order', string='Órdenes de Venta')
    to_use_sale_order_ids = fields.Many2many('sale.order', string='Órdenes de Venta', relation='select_sales_wizard_sale_order_rel',)

    purchase_id = fields.Many2one('purchase.order', string='Pedido de Compra')
    documento = fields.Selection([('cmr', 'CMR'), ('albaran_ventas', 'Albarán de ventas')], 'Documento', default='cmr')


    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        purchase = self.env['purchase.order'].browse(self._context.get('active_id'))
        to_use_sale_order_ids = purchase.order_line.mapped('sale_order_id').filtered(lambda s: s)

        _logger = logging.getLogger(__name__)
        _logger.info(f"Compra obtenida: {purchase.id}, con órdenes de venta: {to_use_sale_order_ids.ids}")
        res.update({
            'purchase_id': purchase.id,
            'to_use_sale_order_ids': to_use_sale_order_ids.ids,
        })
        return res




    # @api.model
    # def default_get(self, fields_list):
    #     res = super().default_get(fields_list)
    #     purchase = self.env['purchase.order'].browse(self._context.get('active_id'))
    #
    #     # Obtener ventas únicas desde las líneas del pedido
    #     sale_orders = purchase.order_line.mapped('sale_order_id')
    #     res.update({
    #         'purchase_id': purchase.id,
    #         'sale_order_ids': [(6, 0, sale_orders.ids)],
    #     })
    #     return res

    def confirm_selection(self):
        if not self.sale_order_ids:
            raise UserError("Debe seleccionar al menos una venta")
        if not self.documento:
            raise UserError("Debe elegir el documento para imprimir")

        purchase = self.purchase_id
        if not purchase:
            raise UserError("No se ha encontrado un pedido de compra relacionado")

        for order in self.sale_order_ids:
            purchase.print_cmr_pdf()







        # pdf_urls = []
        # # pdf = self.env.ref('idealfruit_custom_purchase.action_report_purchaseorder_cmr').report_action(self, data=data)
        # for order in self.sale_order_ids:
        #     datos_pdf= [ {'context_data': 'informacion_1'},]
        #
        #     for idx, data in enumerate(datos_pdf):
        #         # Obtén el PDF como bytes
        #         pdf_data, report_name = self.env.ref('idealfruit_custom_purchase.action_report_purchaseorder_cmr').render_qweb_pdf(self.id, data=data)
        #
        #         # Crear un archivo adjunto con el contenido binario del PDF
        #         attachment = self.env['ir.attachment'].create({
        #             'name': f"pdf_informe_{idx + 1}.pdf",
        #             'type': 'binary',
        #             'datas': base64.b64encode(pdf_data),  # Codifica el archivo en base64
        #             'mimetype': 'application/pdf',
        #         })
        #
        #         # Guardar la URL del archivo adjunto
        #         pdf_urls.append(attachment.public_url)
        #
        #     # Retornar las URLs para que el usuario pueda descargar los tres PDFs
        #     return {
        #         'type': 'ir.actions.act_url',
        #         'url': pdf_urls[0],  # Puedes devolver la primera URL, o mostrarlas todas en una vista
        #         'target': 'self',
        #     }
                # action = self.env.ref('idealfruit_custom_purchase.report_purchaseorder_cmr').sudo()._get_report_action(
            #     self.purchase_id)
            #
            # if not action:
            #     raise UserError("No se ha encontrado la acción del reporte.")
            #
            # return action


