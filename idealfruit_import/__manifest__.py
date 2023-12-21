# Copyright 2023 Manuel Calero (https://xtendoo.es)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Importador de datos de Idealfruit",
    "version": "16.0",
    "author": "Manuel Calero (https://xtendoo.es)",
    "category": "Idealfruit",
    "summary": "Importador de datos de Idealfruit",
    "license": "AGPL-3",
    "depends": [
        "product",
        "contacts",
        "sale_management",
        "purchase",
        "stock",
        "idealfruit_vendor_checklist",
    ],
    "data": [
        "wizard/idealfruit_import_wizard_view.xml",
        "views/idealfruit_import_view.xml",
        "views/purchase_order_view.xml",
        "security/ir.model.access.csv",
    ],
    'installable': True,
    'active': False,
}
