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


class IdealFruitImportCompany(models.TransientModel):
    _name = "idealfruit.import.company"
    _description = "Ideal Fruit Import Company"

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

            self._import_company(book.sheet_by_index(0))

        except xlrd.XLRDError:
            raise ValidationError(
                _("Invalid file style, only .xls or .xlsx file allowed")
            )
        except Exception as e:
            raise e

    def _import_company(self, sheet):
        company_obj = self.env["res.company"]
        country_obj = self.env["res.country"]
        for row in range(1, sheet.nrows):
            ref = sheet.cell(row, 0).value.strip()
            name = sheet.cell(row, 1).value
            vat = sheet.cell(row, 2).value
            country_code = sheet.cell(row, 3).value
            street = sheet.cell(row, 5).value
            mail = sheet.cell(row, 6).value
            company = {
                "company_registry": ref,
                "name": name,
                "street": street,
                "email": mail,
            }
            if vat:
                company["vat"] = country_code + vat
            country_id = country_obj.search([("code", "=", country_code)])

            if country_id:
                company["country_id"] = country_id.id

            company_id = company_obj.search([("name", "=", name)])
            if not company_id:
                company_id = company_obj.create(company)

            if company_id:
                company_id.partner_id.write({
                    "ref": ref,
                    "company_id": company_id.id,
                    "use_only_supplied_product": True,
                })

