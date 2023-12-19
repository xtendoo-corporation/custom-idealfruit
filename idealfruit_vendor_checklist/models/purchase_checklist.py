# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models, api


class PurchaseChecklist(models.Model):
    _name = "purchase.checklist"
    _description = "Purchase Checklist"

    name = fields.Char(
        string="Nombre",
    )
    purchase_checklist_document_ids = fields.One2many(
        comodel_name="purchase.checklist.document",
        inverse_name="purchase_checklist_id",
        string="Documentos",
        required=True,
    )
    purchase_id = fields.One2many(
        comodel_name="purchase.order",
        inverse_name="purchase_checklist_id",
        string="Compra",
    )


class PurchaseChecklistDocument(models.Model):
    _name = "purchase.checklist.document"
    _description = "Purchase Checklist Document"

    name = fields.Char(
        string="Nombre",
    )
    purchase_checklist_id = fields.Many2one(
        comodel_name="purchase.checklist",
        string="Checklist",
    )

    _sql_constraints = [
        ("name_uniq", "UNIQUE(name, purchase_checklist_id)", "El nombre del documento ya existe en el checklist.")]


class PurchaseChecklistDocumentRelation(models.Model):
    _name = "purchase.checklist.document.relation"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Purchase Checklist Document Relation"

    name = fields.Char(
        string="Nombre",
    )
    purchase_order_id = fields.Many2one(
        comodel_name="purchase.order",
        string="Orden de Compra",
    )
    purchase_checklist_id = fields.Many2one(
        comodel_name="purchase.checklist",
        related="purchase_order_id.purchase_checklist_id",
        string="Checklist",
    )
    purchase_checklist_document_id = fields.Many2one(
        comodel_name="purchase.checklist.document",
        domain="[('purchase_checklist_id', '=', purchase_checklist_id)]",
        string="Documentos",
        required=True,
    )
    attachment_ids = fields.One2many(
        comodel_name="ir.attachment",
        inverse_name="res_id",
        string="Adjuntos",
        tracking=True,
    )

    _sql_constraints = [("purchase_uniq", "UNIQUE(purchase_checklist_document_id, purchase_order_id)",
                         "Tipo de documento repetido en el checklist.")]
