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
    quality_document_ids = fields.One2many(
        comodel_name="quality.document",
        inverse_name="purchase_order_id",
        string="Documentos de Calidad",
    )
    quality_document_count = fields.Integer(
        string='Documentos de Calidad Countador',
        compute='_count_quality_document',
        readonly=True)

    def _count_quality_document(self):
        for quality_document in self:
            quality_document.quality_document_count = len(quality_document.quality_document_ids)

    purchase_state = fields.Selection(
        selection=[
            ("invalidated", "No validado"),
            ("validated", "Validado"),
        ],
        string="Situación",
        default="invalidated",
        readonly=True,
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
                print("*", 80)
                print("not purchase.purchase_checklist_id", not purchase.purchase_checklist_id)
                print("*", 80)

                purchase.purchase_state = "invalidated"
                break

            if not purchase.purchase_checklist_document_relation_ids:
                print("*", 80)
                print("purchase.purchase_checklist_document_relation_ids", purchase.purchase_checklist_document_relation_ids)
                print("*", 80)

                purchase.purchase_state = "invalidated"
                break

            mandatory_documents = purchase.purchase_checklist_id.purchase_checklist_document_ids
            print("*", 80)
            print("mandatory_documents", mandatory_documents)
            print("*", 80)

            for document in purchase.purchase_checklist_document_relation_ids:
                print("*", 80)
                print("document", document.purchase_checklist_document_id)
                print("*", 80)

                if document.purchase_checklist_document_id in mandatory_documents:
                    print("*", 80)
                    print("El documento esta en la lista de valores", document.purchase_checklist_document_id)
                    print("document.attachment_ids", document.attachment_ids)
                    print("*", 80)
                    if not document.attachment_ids:
                        purchase.purchase_state = "invalidated"
                    else:
                        purchase.purchase_state = "validated"
                        mandatory_documents = mandatory_documents - document.purchase_checklist_document_id

                        print("*", 80)
                        print("mandatory_documents", mandatory_documents)
                        print("*", 80)

                if mandatory_documents:
                    purchase.purchase_state = "invalidated"
                else:
                    purchase.purchase_state = "validated"

    def open_quality_document(self):
        self.ensure_one()
        return {
            'name': 'Documentos de la plantilla de calidad',
            'view_mode': 'tree,form',
            'views': [(self.env.ref('idealfruit_vendor_checklist.view_quality_document_tree').id, 'tree'), (False, 'form')],
            'res_model': 'quality.document',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [
                ('purchase_order_id', '=', self.id)
            ],
            'context': {
                'default_purchase_order_id': self.id,
            },
        }
