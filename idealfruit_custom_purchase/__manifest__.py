# Copyright 2021 ForgeFlow (http://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

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
    ],
    "data": [
        'security/ir.model.access.csv',
        'security/security_groups.xml',
        'views/palet_type_views.xml',
        'views/purchase_order_line_views.xml',
    ],
    "license": "LGPL-3",
    "installable": True,
}
