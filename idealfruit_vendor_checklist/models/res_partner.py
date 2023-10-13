# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    vendor_checklist_id = fields.Many2one(
        comodel_name="vendor.checklist",
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
        string="Situación",
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
                            "name": document.name,
                            "vendor_checklist_document_id": document.id,
                        },
                    )
                ]

    @api.onchange("vendor_checklist_id","vendor_checklist_document_relation_ids")
    def check_vendor_state(self):
        for record in self:
            if not record.vendor_checklist_id:
                record.vendor_state = "invalidated"
                break

            if not record.vendor_checklist_document_relation_ids:
                record.vendor_state = "invalidated"
                break

            mandatory_documents = record.vendor_checklist_id.vendor_checklist_document_ids.filtered(lambda d: d.is_mandatory)

            for document in record.vendor_checklist_document_relation_ids:
                print("*", 80)
                print("document", document.vendor_checklist_document_id)
                print("*", 80)

                if document.vendor_checklist_document_id in mandatory_documents:
                    if not document.date_validated or document.date_validated > fields.Date.today() or not document.attachment_ids:
                        record.vendor_state = "invalidated"
                        break

                record.vendor_state = "validated"
