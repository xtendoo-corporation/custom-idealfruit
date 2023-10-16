# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models, api


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
        is_mandatory=True,
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
    is_mandatory = fields.Boolean(
        string="Requerido",
        default=True,
    )

    _sql_constraints = [
        ("name_uniq", "UNIQUE(name, vendor_checklist_id)", "El nombre del documento ya existe en el checklist.")]


class VendorChecklistDocumentRelation(models.Model):
    _name = "vendor.checklist.document.relation"
    _description = "Vendor Checklist Document Relation"

    name = fields.Char(
        string="Nombre",
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Proveedor",
    )
    vendor_checklist_id = fields.Many2one(
        comodel_name="vendor.checklist",
        related="partner_id.vendor_checklist_id",
        string="Checklist",
    )
    vendor_checklist_document_id = fields.Many2one(
        comodel_name="vendor.checklist.document",
        domain="[('vendor_checklist_id', '=', vendor_checklist_id)]",
        string="Documento",
        required=True,
    )
    date_validated = fields.Date(
        string="Fecha de Validez",
    )
    attachment_ids = fields.One2many(
        comodel_name="ir.attachment",
        inverse_name="res_id",
        string="Adjuntos",
        tracking=True,
    )
    is_validated = fields.Boolean(
        string="Validado",
        compute="_compute_is_validated",
    )

    @api.depends("date_validated", "attachment_ids")
    def _compute_is_validated(self):
        for record in self:
            record.is_validated = record.date_validated and record.date_validated >= fields.Date.today() and record.attachment_ids

    _sql_constraints = [("checklist_uniq", "UNIQUE(partner_id, vendor_checklist_document_id)",
                         "El tipo de documento ya existe en el checklist.")]
