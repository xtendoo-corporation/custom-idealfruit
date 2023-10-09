# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class VendorChecklist(models.Model):
    _name = "vendor.checklist"
    _description = "Vendor Checklist"

    name = fields.Char(
        string="Nombre",
    )
    vendor_checklist_document_ids = fields.One2many(
        comodel_name="vendor.checklist.document",
        inverse_name="vendor_checklist_id",
        string="Documentos",
    )
    partner_id = fields.One2many(
        comodel_name="res.partner",
        inverse_name="vendor_checklist_id",
        string="Proveedor",
    )


class VendorChecklistDocument(models.Model):
    _name = "vendor.checklist.document"
    _description = "Vendor Checklist Document"

    name = fields.Char(
        string="Nombre",
    )
    vendor_checklist_id = fields.Many2one(
        comodel_name="vendor.checklist",
        string="Checklist",
    )

    _sql_constraints = [("name_uniq", "UNIQUE(name, vendor_checklist_id)", "El nombre del documento ya existe en el checklist.")]


class VendorChecklistDocumentRelation(models.Model):
    _name = "vendor.checklist.document.relation"
    _description = "Vendor Checklist Document Relation"

    name = fields.Char(
        string="Nombre",
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        inverse_name="vendor_checklist_document_relation_ids",
        string="Proveedor",
    )
    vendor_checklist_document_id = fields.Many2one(
        comodel_name="vendor.checklist.document",
        string="Checklist",
    )
    date_validated = fields.Date(
        string="Fecha de Validez",
    )










