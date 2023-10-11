# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Ideal Fruit Vendor Checklist",
    "version": "16.0.1.0.1",
    "development_status": "Mature",
    "category": "Product",
    "summary": "Ideal Fruit Vendor Checklist",
    "author": "Xtendoo, ",
    "website": "https://github.com/xtendoo-corporation/",
    "license": "AGPL-3",
    "depends": [
        "purchase",
        "odx_m2m_attachment_preview",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/cron.xml",
        "views/vendor_checklist_view.xml",
        "views/purchase_checklist_view.xml",
        "views/res_partner_view.xml",
        "views/purchase_order_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
