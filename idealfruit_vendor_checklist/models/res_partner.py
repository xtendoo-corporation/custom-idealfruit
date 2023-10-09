# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    vendor_checklist_id = fields.Many2one(
        comodel_name="vendor.checklist",
        inverse_name="partner_id",
        string="Checklist",
    )
    vendor_checklist_document_relation_ids = fields.One2many(
        comodel_name="vendor.checklist.document.relation",
        inverse_name="partner_id",
        string="Checklist",
    )
    vendor_state = fields.Selection(
        selection=[
            ("invalidated", "No validado"),
            ("validated", "Validado"),
        ],
        string="Estado",
        default="invalidated",
    )

    @api.onchange("vendor_checklist_id")
    def _onchange_vendor_checklist_id(self):
        for record in self:
            record.vendor_checklist_document_relation_ids = [(5, 0, 0)]
            for document in record.vendor_checklist_id.vendor_checklist_document_ids:
                record.vendor_checklist_document_relation_ids = [
                    (
                        0,
                        0,
                        {
                            "vendor_checklist_document_id": document.id,
                            "name": document.name,
                        },
                    )
                ]

    def check_vendor_state(self):
        for record in self:
            if record.vendor_checklist_document_relation_ids:
                for document in record.vendor_checklist_document_relation_ids:
                    if not document.date_validated or document.date_validated > fields.Date.today():
                        record.vendor_state = "invalidated"
                        break
                    else:
                        record.vendor_state = "validated"
            else:
                record.vendor_state = "invalidated"
