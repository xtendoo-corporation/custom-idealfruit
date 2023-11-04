# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models, api


class PurchaseQuality(models.Model):
    _name = "purchase.quality"
    _description = "Purchase Quality"

    name = fields.Char(
        string="Nombre",
    )
    lead_properties_definition = fields.PropertiesDefinition(
        'Lead Properties'
    )

