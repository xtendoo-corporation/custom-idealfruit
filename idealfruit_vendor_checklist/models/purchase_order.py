# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    purchase_checklist_id = fields.Many2one(
        comodel_name="purchase.checklist",
        string="Checklist",
    )
    purchase_checklist_document_relation_ids = fields.One2many(
        comodel_name="purchase.checklist.document.relation",
        inverse_name="purchase_order_id",
        string="Documentos",
        tracking=True,
    )

    purchase_state = fields.Selection(
        selection=[
            ("invalidated", "No validado"),
            ("validated", "Validado"),
        ],
        string="Situación",
        default="invalidated",
        readonly=True,
    )
    purchase_order_quality_doc_ids = fields.One2many(
        comodel_name="purchase.order.quality.doc",
        inverse_name="purchase_order_id",
        string="Documentos de Calidad",
    )

    @api.onchange("purchase_checklist_id")
    def _onchange_purchase_checklist_id(self):
        for purchase in self:
            purchase.purchase_checklist_document_relation_ids = [(5, 0, 0)]
            for document in purchase.purchase_checklist_id.purchase_checklist_document_ids:
                purchase.purchase_checklist_document_relation_ids = [
                    (
                        0,
                        0,
                        {
                            "name": document.name,
                            "purchase_checklist_document_id": document.id,
                        },
                    )
                ]

    @api.onchange("purchase_checklist_id","purchase_checklist_document_relation_ids")
    def check_purchase_state(self):
        for purchase in self:
            if not purchase.purchase_checklist_id:
                purchase.purchase_state = "invalidated"
                break

            if not purchase.purchase_checklist_document_relation_ids:
                purchase.purchase_state = "invalidated"
                break

            required_documents = purchase.purchase_checklist_id.purchase_checklist_document_ids
            for document in purchase.purchase_checklist_document_relation_ids:
                if document.purchase_checklist_document_id in required_documents:
                    if not document.attachment_ids:
                        purchase.purchase_state = "invalidated"
                    else:
                        purchase.purchase_state = "validated"
                        required_documents = required_documents - document.purchase_checklist_document_id
                if required_documents:
                    purchase.purchase_state = "invalidated"
                else:
                    purchase.purchase_state = "validated"

