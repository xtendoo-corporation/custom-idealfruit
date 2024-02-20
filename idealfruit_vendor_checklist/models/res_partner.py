# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import re
from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError

class ResPartner(models.Model):
    _inherit = "res.partner"

    vendor_checklist_id = fields.Many2one(
        comodel_name="vendor.checklist",
        string="Checklist",
    )
    vendor_checklist_document_relation_ids = fields.One2many(
        comodel_name="vendor.checklist.document.relation",
        inverse_name="partner_id",
        string="Documentos",
        tracking=True,
    )
    vendor_state = fields.Selection(
        selection=[
            ("invalidated", "No validado"),
            ("validated", "Validado"),
        ],
        string="Situación",
        default="invalidated",
    )
    type = fields.Selection(
        selection_add=[("productor", "Productor")],
        default="productor",
        ondelete={"contact": "cascade"},
    )
    global_gap = fields.Char(
        string="Global Gap",
    )
    a3_code = fields.Char(
        string="Código A3",
    )
    trace_code = fields.Char(
        string='Código trazabilidad',
    )

    @api.model
    def create(self, vals):
        # Get the group
        group = self.env.ref('idealfruit_record_rule.idealfruit_group_supplier')

        print("=====================================")
        print("vals: ", vals)
        print("vals['type']: ", vals['type'])
        print("vals['is_company']", vals['is_company'])

        # Check if the current user is in the group
        if vals['is_company'] and group in self.env.user.groups_id:
            raise UserError("No tiene permisos para crear nuevos partners.")

        # If the user is not in the group, proceed with the creation
        return super(ResPartner, self).create(vals)


    @api.constrains('global_gap')
    def _check_global_gap(self):
        for record in self.filtered(lambda r: not r.is_company and r.type == 'productor'):
            if record.global_gap and not re.match("^[0-9]+$", record.global_gap):
                raise ValidationError("El campo debe contener solo valores numéricos.")
            if not record.global_gap:
                raise ValidationError("El campo Global Gap es requerido para los productores.")
            if self.env['res.partner'].search_count(
                [('parent_id', '=', record.parent_id), ('global_gap', '=', record.global_gap), ('id', '!=', record.id)]
            ) > 0:
                raise ValidationError("El campo Global Gap del productor debe ser único.")

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

    @api.onchange("vendor_checklist_id", "vendor_checklist_document_relation_ids")
    def check_vendor_state(self):
        for record in self:
            if not record.vendor_checklist_id:
                print("*", 80)
                print("not record.vendor_checklist_id", not record.vendor_checklist_id)
                print("*", 80)
                record.vendor_state = "invalidated"
                break

            if not record.vendor_checklist_document_relation_ids:
                print("*", 80)
                print("record.vendor_checklist_document_relation_ids", record.vendor_checklist_document_relation_ids)
                print("*", 80)
                record.vendor_state = "invalidated"
                break

            required_documents = record.vendor_checklist_id.vendor_checklist_document_ids.filtered(
                lambda d: d.is_required)
            print("*", 80)
            print("required_documents", required_documents)
            print("*", 80)

            for document in record.vendor_checklist_document_relation_ids:
                print("*", 80)
                print("document", document.vendor_checklist_document_id)
                print("*", 80)
                if document.vendor_checklist_document_id in required_documents:
                    print("*", 80)
                    print("El documento esta en la lista de valores", document.vendor_checklist_document_id)
                    print("document.date_validated", document.date_validated)
                    print("document.attachment_ids", document.attachment_ids)
                    print("*", 80)
                    if not document.date_validated or document.date_validated < fields.Date.today() or not document.attachment_ids:
                        print("not document.date_validated", not document.date_validated)
                        print("not document.attachment_ids", not document.attachment_ids)
                        print("El documento esta invalidated")

                        record.vendor_state = "invalidated"
                    else:
                        print("*", 80)
                        print("El documento esta validated")
                        print("*", 80)
                        record.vendor_state = "validated"
                        required_documents = required_documents - document.vendor_checklist_document_id

                        print("*", 80)
                        print("required_documents", required_documents)
                        print("*", 80)

                if required_documents:
                    record.vendor_state = "invalidated"

    @api.model
    def _cron_recurring_validated(self):
        email = self.env['ir.config_parameter'].sudo().get_param('idealfruit_vendor_checklist.idealfruit_vendor_email')
        if not email:
            return
        partners = self.env['res.partner'].search(
            [
                '|', ('is_company', '=', True),
                ('type', '=', 'productor'), ('supplier_rank', '>', 0),
                ('vendor_state', '=', 'invalidated')
            ]
        )
        if partners:
            template_id = self.env.ref('idealfruit_vendor_checklist.idealfruit_vendor_invalidated')
            if not template_id:
                return
            template = self.env['mail.template'].browse(template_id.id)
            template.write({'email_to': email})
            template.with_context({'partners': partners}).send_mail(self.id, force_send=True)

    @api.model
    def cron_recurring_validated(self):
        return self._cron_recurring_validated()
