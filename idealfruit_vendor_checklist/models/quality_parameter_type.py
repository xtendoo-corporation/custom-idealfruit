# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models, api


class QualityParameterType(models.Model):
    _name = "quality.parameter.type"
    _description = "Tipos de Parámetros de Calidad"

    name = fields.Char(
        string="Nombre",
        required=True,
    )
    percentage_application = fields.Float(
        string="Porcentaje de aplicación",
        required=True,
    )
