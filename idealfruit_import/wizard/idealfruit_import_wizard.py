# Copyright 2023 Manuel Calero
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import base64
import xlrd

from odoo import _, fields, api, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

try:
    from csv import reader
except (ImportError, IOError) as err:
    _logger.error(err)


class IdealFruitImport(models.TransientModel):
    _name = "idealfruit.import"
    _description = "Ideal Fruit Import"

    import_file = fields.Binary(
        string="Import File (*.xlsx)",
    )

    def action_import_file(self):
        """ Process the file chosen in the wizard, create bank statement(s) and go to reconciliation. """
        self.ensure_one()
        if self.import_file:
            self._import_record_data(self.import_file)
        else:
            raise ValidationError(_("Please select Excel file to import"))

    @api.model
    def _import_record_data(self, import_file):
        try:
            decoded_data = base64.decodebytes(import_file)
            book = xlrd.open_workbook(file_contents=decoded_data)

            self._import_supplier(book.sheet_by_index(0))
            self._import_supplier_contacts(book.sheet_by_index(1))
            self._import_categories(book.sheet_by_index(2))
            self._import_products(book.sheet_by_index(3))
            self._import_product_supplier_info(book.sheet_by_index(4))

        except xlrd.XLRDError:
            raise ValidationError(
                _("Invalid file style, only .xls or .xlsx file allowed")
            )
        except Exception as e:
            raise e

    def _import_supplier(self, sheet):
        partner_obj = self.env["res.partner"]
        country_obj = self.env["res.country"]
        for row in range(1, sheet.nrows):
            ref = sheet.cell(row, 0).value.strip()
            name = sheet.cell(row, 1).value
            vat = sheet.cell(row, 2).value
            country_code = sheet.cell(row, 3).value
            street = sheet.cell(row, 5).value
            mail = sheet.cell(row, 6).value

            partner = {
                "company_type": 'company',
                "ref": ref,
                "name": name,
                "street": street,
                "email": mail,
            }

            if vat:
                partner["vat"] = country_code + vat

            country_id = country_obj.search([("code", "=", country_code)])
            if country_id:
                partner["country_id"] = country_id.id

            partner_id = partner_obj.search([("ref", "=", ref)])
            if partner_id:
                partner_id.write(partner)
            else:
                partner_obj.create(partner)

    def _import_supplier_contacts(self, sheet):
        partner_obj = self.env["res.partner"]
        country_obj = self.env["res.country"]
        for row in range(1, sheet.nrows):
            ref = sheet.cell(row, 0).value.strip()
            a3_code = sheet.cell(row, 1).value.strip()
            trace_code = sheet.cell(row, 2).value.strip()
            name = sheet.cell(row, 3).value.strip()
            global_gap = sheet.cell(row, 4).value
            country_code = sheet.cell(row, 5).value
            full_default_code = ref + " " + trace_code

            parent_id = partner_obj.search([("ref", "=", ref)])
            if parent_id:
                partner_contact = {
                    "company_type": 'person',
                    "type": "productor",
                    "trace_code": trace_code,
                    "parent_id": parent_id.id,
                    "ref": full_default_code,
                    "name": name,
                    "global_gap": global_gap,
                    "a3_code": a3_code,
                }
                if country_code:
                    country_id = country_obj.search([("code", "=", country_code)])
                    if country_id:
                        partner_contact["country_id"] = country_id.id

                partner_id = partner_obj.search([("ref", "=", full_default_code)])
                if partner_id:
                    partner_id.write(partner_contact)
                else:
                    partner_obj.create(partner_contact)

    def _import_categories(self, sheet):
        category_obj = self.env["product.category"]
        for row in range(1, sheet.nrows):
            default_code = sheet.cell(row, 0).value.strip()
            name = sheet.cell(row, 1).value.strip()
            category_id = category_obj.search([("default_code", "=", default_code)])
            if not category_id:
                category_obj.create({
                    "default_code": default_code,
                    "name": name,
                })

    def _import_products(self, sheet):
        product_obj = self.env["product.template"]
        category_obj = self.env["product.category"]
        for row in range(1, sheet.nrows):
            default_code = sheet.cell(row, 0).value.strip()
            name = sheet.cell(row, 1).value.strip()
            is_bulk = sheet.cell(row, 2).value == "T"
            weight = sheet.cell(row, 3).value.replace(",", ".")
            unit_box = sheet.cell(row, 4).value
            category_code = sheet.cell(row, 5).value.strip()
            is_ecological = sheet.cell(row, 6).value == "T"

            product_template = {
                "default_code": default_code,
                "name": name,
                "is_bulk": is_bulk,
                "weight": weight,
                "unit_box": unit_box,
                "is_ecological": is_ecological,
            }

            category_id = category_obj.search([("default_code", "=", category_code)])
            if category_id:
                product_template["categ_id"] = category_id.id

            product_id = product_obj.search([("default_code", "=", default_code)])
            if not product_id:
                product_obj.create(product_template)
            else:
                product_id.write(product_template)

    def _import_product_supplier_info(self, sheet):
        partner_obj = self.env["res.partner"]
        product_obj = self.env["product.template"]
        for row in range(1, sheet.nrows):
            ref = sheet.cell(row, 0).value.strip()
            default_code = sheet.cell(row, 2).value.strip()

            partner_id = partner_obj.search(
                [("ref", "=", ref)]
            )
            product_template_id = product_obj.search(
                [("default_code", "=", default_code)]
            )
            if partner_id and product_template_id:
                if not self.env["product.supplierinfo"].search(
                    [
                        ("partner_id", "=", partner_id.id),
                        ("product_tmpl_id", "=", product_template_id.id),
                    ]
                ):
                    self.env["product.supplierinfo"].create(
                        {
                            "partner_id": partner_id.id,
                            "product_tmpl_id": product_template_id.id,
                        }
                    )
