# Copyright 2023 Camilo Prado (https://xtendoo.es)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Importador de datos de Idealfruit",
    "version": "16.0",
    "author": "Manuel Calero (https://xtendoo.es)",
    "category": "Idealfruit",
    "license": "AGPL-3",
    "depends": [
        "product",
        "contacts",
        "sale",
        "purchase",
    ],
    "data": [
        "wizard/import_wizard_view.xml",
        "views/calatayud_product_import_view.xml",
        "security/ir.model.access.csv",
    ],
    'installable': True,
    'active': False,
}
