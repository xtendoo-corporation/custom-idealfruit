from odoo import models, api, fields


class PaletCategory(models.Model):
    _name = 'palet.category'
    _description = 'Palet category'

    name = fields.Char(string='Nombre', required=True)
    description = fields.Text(string='Descripción')
    length = fields.Float(string='Largo', required=True)
    width = fields.Float(string='ancho', required=True)
    height = fields.Float(string='Alto', required=True)
    udm = fields.Many2one('uom.uom', string='UDM Medidas', required=True,default=lambda self: self.env.ref('uom.product_uom_meter'))

