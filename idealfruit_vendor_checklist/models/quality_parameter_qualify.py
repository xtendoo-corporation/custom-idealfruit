# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models, api


class QualityParameterQualify(models.Model):
    _name = "quality.parameter.qualify"
    _description = "Calificación de Parámetros de Calidad"

    name = fields.Char(
        string="Nombre",
        required=True,
    )


