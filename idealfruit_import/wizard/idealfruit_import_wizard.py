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
                "vat": country_code + vat,
                "street": street,
                "email": mail,
            }
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
            trace = sheet.cell(row, 2).value.strip()
            name = sheet.cell(row, 3).value.strip()
            global_gap = sheet.cell(row, 4).value
            country_code = sheet.cell(row, 5).value
            full_ref = ref + " " + trace

            parent_id = partner_obj.search([("ref", "=", ref)])
            if parent_id:
                partner_contact = {
                    "company_type": 'person',
                    "type": "productor",
                    "parent_id": parent_id.id,
                    "ref": full_ref,
                    "name": name,
                    "global_gap": global_gap,
                    "a3_code": a3_code,
                }
                if country_code:
                    country_id = country_obj.search([("code", "=", country_code)])
                    if country_id:
                        partner_contact["country_id"] = country_id.id

                partner_id = partner_obj.search([("ref", "=", full_ref)])
                if partner_id:
                    partner_id.write(partner_contact)
                else:
                    partner_obj.create(partner_contact)

    def _import_categories(self, sheet):
        category_obj = self.env["product.category"]
        for row in range(1, sheet.nrows):
            name = sheet.cell(row, 1).value.strip() + " (" + sheet.cell(row, 0).value.strip() + ")"
            category_id = category_obj.search([("name", "=", name)])
            if not category_id:
                category_obj.create({"name": name})

    def _import_products(self, sheet):
        product_obj = self.env["product.template"]
        category_obj = self.env["product.category"]
        uom_obj = self.env["uom.uom"]
        for row in range(1, sheet.nrows):
            ref = sheet.cell(row, 0).value.strip()
            name = sheet.cell(row, 1).value.strip()
            category_code = "%(" + sheet.cell(row, 5).value.strip() + ")"
            category_id = category_obj.search([("name", "like", category_code)])

            uom_id = uom_obj.search([("name", "=", uom_name)])
            if category_id and uom_id:
                product_id = product_obj.search([("name", "=", name)])
                if not product_id:
                    product_obj.create({
                        "name": name,
                        "categ_id": category_id.id,
                        "uom_id": uom_id.id,
                        "uom_po_id": uom_id.id,
                        "list_price": price,
                    })
