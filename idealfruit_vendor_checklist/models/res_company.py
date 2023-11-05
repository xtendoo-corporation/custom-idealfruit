# Copyright 2023 Manuel Calero <manuelcalero@xtendoo.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class Company(models.Model):
    _inherit = 'res.company'

    def _create_quality_document_sequence(self):
        vals = []
        for company in self:
            vals.append({
                'name': 'Contador de documentos de calidad',
                'code': 'quality.document',
                'company_id': company.id,
                'prefix': 'QUA/%(year)s/',
                'padding': 5,
                'number_next': 1,
                'number_increment': 1
            })
        if vals:
            self.env['ir.sequence'].create(vals)

    @api.model
    def create_quality_document_sequence(self):
        company_ids = self.env['res.company'].search([])
        company_has_quality_document = self.env['ir.sequence'].search(
            [('code', '=', 'quality.document')]).mapped('company_id')
        company_todo_sequence = company_ids - company_has_quality_document
        company_todo_sequence._create_quality_document_sequence()
