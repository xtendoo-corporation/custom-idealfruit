from odoo import fields, models, api

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    idealfruit_vendor_email = fields.Char(
        string="Email",
        config_parameter="idealfruit_vendor_checklist.idealfruit_vendor_email",
    )
