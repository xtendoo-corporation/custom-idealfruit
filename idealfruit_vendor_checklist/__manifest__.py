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
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/data.xml",
        "data/cron.xml",
        "data/email_template.xml",
        "views/vendor_checklist_view.xml",
        "views/purchase_checklist_view.xml",
        "views/template_quality_view.xml",
        "views/res_partner_view.xml",
        "views/purchase_order_view.xml",
        "views/idealfruit_format_view.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
