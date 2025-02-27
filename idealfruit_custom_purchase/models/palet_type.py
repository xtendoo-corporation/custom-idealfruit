from odoo import models, api, fields


class PaletType(models.Model):
    _name = 'palet.type'
    _description = 'Palet Type'

    name = fields.Char(string='Nombre', required=True)
    description = fields.Text(string='Descripción')
    weight = fields.Float(string='Peso', required=True)
    weight_udm = fields.Many2one('uom.uom', string='UDM Peso', required=True,default=lambda self: self.env.ref('uom.product_uom_meter'))

    palet_category_id = fields.Many2one(
        'palet.category',
        string='Categoría de Palet',
        required=True
    )
    length = fields.Float(string='Largo', related='palet_category_id.length', store=True)
    # length_udm = fields.Many2one('uom.uom', 'name', string='UDM Largo', required=True, related='palet_category_id.length_udm', store=True)
    width = fields.Float(string='ancho', related='palet_category_id.width', store=True)
    # width_udm = fields.Many2one('uom.uom', 'name', string='UDM Ancho', required=True, related='palet_category_id.width_udm', store=True)
    height = fields.Float(string='Alto', related='palet_category_id.height', store=True)
    udm = fields.Many2one('uom.uom', string='UDM Medidas', required=True, related='palet_category_id.udm', store=True)

