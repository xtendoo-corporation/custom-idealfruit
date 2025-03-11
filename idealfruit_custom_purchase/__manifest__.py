# Copyright 2021 ForgeFlow (http://www.forgeflow.com)
{
    "name": "IdealFruit Custom Purchase",
    "author": "Dani Domninguez",
    "company": "Xtendoo",
    "summary": "IdealFruit Custom Purchase",
    "version": "16.0.1.0.0",
    "category": "Extra-tools",
    "website": "https://xtendoo.es",
    "depends": [
        "base",
        "purchase",
        "idealfruit_product_variety",
        "idealfruit_vendor_checklist",
        "web",
    ],
    "data": [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/purchase_line_productor_views.xml',
        'views/purchase_line_indications_views.xml',
        'views/palet_type_views.xml',
        'views/palet_category_views.xml',
        'views/purchase_order_line_views.xml',
        'data/palet_category_data.xml',
        'views/cmr_docs/layout_cmr.xml',
        'views/cmr_docs/layout_empty.xml',
        'views/cmr_docs/albaran_venta_report.xml',
        'views/cmr_docs/cmr_report.xml',
        'views/cmr_docs/control_mercancia_report.xml',

    ],
    "license": "LGPL-3",
    "installable": True,
}
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

