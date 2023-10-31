# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models, api


class PurchaseQuality(models.Model):
    _name = "purchase.quality"
    _description = "Purchase Quality"

    name = fields.Char(
        string="Nombre",
    )
    # purchase_quality_id = fields.Many2one(
    #     comodel_name="purchase.order",
    #     string="Orden de Compra",
    # )
    lead_properties_definition = fields.PropertiesDefinition('Lead Properties')
