# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    purchase_checklist_document_relation_ids = fields.One2many(
        comodel_name="purchase.checklist.document.relation",
        inverse_name="purchase_order_id",
        string="Purchase Checklist",
    )
    purchase_state = fields.Selection(
        selection=[
            ("invalidated", "No validado"),
            ("validated", "Validado"),
        ],
        string="Situacion Compra",
        default="invalidated",
        readonly=True,
    )

    @api.onchange("purchase_checklist_document_relation_ids")
    def check_purchase_state(self):
        documents = self.env["purchase.checklist.document"].search([])  # [1,2,3]
        for purchase in self:
            if (purchase.purchase_checklist_document_relation_ids
                and len(documents) == len(purchase.purchase_checklist_document_relation_ids)):
                for document in purchase.purchase_checklist_document_relation_ids:
                    if document.purchase_checklist_document_id not in documents or not document.attachment_ids:
                        purchase.purchase_state = "invalidated"
                        break
                    else:
                        purchase.purchase_state = "validated"
            else:
                purchase.purchase_state = "invalidated"
