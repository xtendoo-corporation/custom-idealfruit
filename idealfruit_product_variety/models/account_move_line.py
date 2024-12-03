from odoo import models, fields

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    product_variety_id = fields.Many2one(
        comodel_name='product.variety',
        string='Product Variety'
    )
