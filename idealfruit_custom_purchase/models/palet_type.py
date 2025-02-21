from odoo import models, api, fields


class PaletType(models.Model):
    _name = 'palet.type'
    _description = 'Palet Type'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
