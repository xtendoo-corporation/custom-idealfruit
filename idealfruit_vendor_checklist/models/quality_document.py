# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class QualityDocument(models.Model):
    _name = "quality.document"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = "Documentos de calidad"

    name = fields.Char(
        string='Número',
        required=True,
        index=True,
        copy=False,
        default="New",
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        required=True,
        default=lambda self: self.env.company,
    )
    datetime = fields.Datetime(
        string="Fecha",
        required=True,
        default=fields.Datetime.now,
    )
    purchase_order_id = fields.Many2one(
        comodel_name="purchase.order",
        string="Pedido",
    )
    purchase_order_line_ids = fields.One2many(
        comodel_name="purchase.order.line",
        related="purchase_order_id.order_line",
        string="Líneas de pedido de compra",
    )
    quality_template_id = fields.Many2one(
        comodel_name="quality.template",
        string="Plantilla",
        required=True,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Producto",
        domain="[('id', 'in', allowed_product_ids)]",
    )
    allowed_product_ids = fields.Many2many(
        comodel_name="product.product",
        string="Allowed products",
        compute="_compute_allowed_product_ids",
    )
    res_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Productor",
        domain="[('id', 'in', allowed_partner_ids)]",
    )
    allowed_partner_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Allowed partners",
        compute="_compute_allowed_partners_ids",
    )
    quality_document_line_ids = fields.One2many(
        comodel_name="quality.document.line",
        inverse_name="quality_document_id",
        string="Líneas",
    )
    net_weight = fields.Float(
        string="Peso neto",
    )
    firmness_units = fields.Float(
        string="Unidades de firmeza",
    )
    appearance_units = fields.Float(
        string="Unidades de apariencia",
    )

    @api.model
    def create(self, vals):
        if vals.get("name", "New") == "New":
            vals["name"] = self._prepare_name(vals)
        return super().create(vals)

    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        if "name" not in default:
            default["name"] = self._prepare_name(default)
        return super().copy(default)

    def _prepare_name(self, values):
        seq = self.env["ir.sequence"]
        if "company_id" in values:
            seq = seq.with_company(values["company_id"])
        return seq.next_by_code("quality.document") or "New"

    @api.depends("purchase_order_id.order_line")
    def _compute_allowed_product_ids(self):
        for quality_document in self:
            quality_document.allowed_product_ids = quality_document.purchase_order_id.order_line.mapped("product_id")

    @api.depends("purchase_order_id.order_line")
    def _compute_allowed_partners_ids(self):
        for quality_document in self:
            quality_document.allowed_partner_ids = quality_document.purchase_order_id.order_line.mapped("product_partner_id")

    @api.onchange("product_id")
    def _onchange_product_id(self):
        for document in self:
            document.quality_template_id = document.product_id.quality_template_id

    @api.onchange("quality_template_id")
    def _onchange_quality_template_id(self):
        for document in self:
            document.quality_document_line_ids = [(5, 0, 0)]
            for line in document.quality_template_id.quality_template_line_ids:
                document.quality_document_line_ids = [
                    (0, 0, { "parameter_id": line.parameter_id})
                ]

