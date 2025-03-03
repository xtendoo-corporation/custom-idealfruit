# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    purchase_checklist_id = fields.Many2one(
        comodel_name="purchase.checklist",
        string="Checklist",
    )
    purchase_checklist_document_relation_ids = fields.One2many(
        comodel_name="purchase.checklist.document.relation",
        inverse_name="purchase_order_id",
        string="Documentos",
        tracking=True,
    )
    purchase_state = fields.Selection(
        selection=[
            ("need_doc", "Documentación Incompleta"),
            ("invalidated", "Esperando validación..."),
            ("validated", "Documentación completa"),
        ],
        string="Situación",
        default="need_doc",
        readonly=True,
        tracking=True,
    )
    purchase_order_quality_doc_ids = fields.One2many(
        comodel_name="purchase.order.quality.doc",
        inverse_name="purchase_order_id",
        string="Documentos de Calidad",
    )
    is_partner_set = fields.Boolean(
        string="Partner Set",
        compute="_compute_is_partner_set",
        store=True,
    )

    @api.onchange("purchase_checklist_id")
    def _onchange_purchase_checklist_id(self):
        for purchase in self:
            purchase.purchase_checklist_document_relation_ids = [(5, 0, 0)]
            for document in purchase.purchase_checklist_id.purchase_checklist_document_ids:
                purchase.purchase_checklist_document_relation_ids = [
                    (
                        0,
                        0,
                        {
                            "name": document.name,
                            "purchase_checklist_document_id": document.id,
                        },
                    )
                ]

    @api.onchange("purchase_checklist_id","purchase_checklist_document_relation_ids")
    def check_purchase_state(self):
        for purchase in self:
            if not purchase.purchase_checklist_id:
                purchase.purchase_state = "need_doc"
                break
            elif not purchase.purchase_checklist_document_relation_ids:
                purchase.purchase_state = "need_doc"
                break
            else:
                required_documents = purchase.purchase_checklist_id.purchase_checklist_document_ids
                for document in purchase.purchase_checklist_document_relation_ids:
                    if document.purchase_checklist_document_id in required_documents:
                        if not document.attachment_ids:
                            purchase.purchase_state = "need_doc"
                        else:
                            purchase.purchase_state = "invalidated"
                self._send_mail_checklist()

    @api.depends("partner_id")
    def _compute_is_partner_set(self):
        for purchase in self:
            purchase.is_partner_set = bool(purchase.partner_id)

    def _send_mail_checklist(self):
        body_html = ""
        purchase_id = str(self.id)
        if "_" in purchase_id:
            purchase_id = purchase_id.split("_")[1]
        purchase_link_base = self.env['ir.config_parameter'].sudo().get_param('notification.base.url')
        if not purchase_link_base:
            raise UserError("No se ha configurado el parámetro del sistema 'notification.base.url'")
        purchase_link = f"{purchase_link_base}/web#id={purchase_id}&cids=1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11%2C12%2C13%2C14%2C15%2C16%2C17%2C18%2C19%2C20%2C21%2C22%2C23%2C24%2C25%2C26%2C27%2C28%2C29%2C30%2C31%2C32%2C33%2C34%2C35%2C36%2C37%2C38%2C39%2C40%2C41%2C42%2C43%2C44%2C45%2C46%2C47%2C48%2C49%2C50%2C51%2C52%2C53%2C54%2C55%2C56%2C57%2C58%2C59%2C60%2C61%2C62%2C63%2C64%2C65%2C66%2C67%2C68%2C69%2C70%2C71%2C72%2C73%2C74%2C75%2C76%2C77%2C78%2C79%2C80%2C81%2C82%2C83%2C84%2C85%2C86%2C87%2C88%2C89%2C90%2C91%2C92%2C93%2C94%2C95%2C96%2C97%2C98%2C99%2C100%2C101%2C102%2C103%2C104%2C105%2C106%2C107%2C108%2C109%2C110%2C111%2C112%2C113%2C114%2C115%2C116%2C117%2C118%2C119%2C120%2C121%2C122%2C123%2C162%2C163%2C164%2C165%2C166%2C167%2C168%2C169%2C170%2C171%2C172%2C173%2C174%2C175%2C176%2C177%2C178%2C179%2C180%2C181%2C182%2C183%2C184%2C185%2C186%2C187%2C188%2C189%2C190%2C191%2C192%2C193&menu_id=245&action=355&model=purchase.order&view_type=form"
        if self.purchase_state == "invalidated":
            users_to_notify = self.env['res.users'].search([('groups_id', 'in', self.env.ref('idealfruit_vendor_checklist.group_purchase_checklist_validator').id)])
        elif self.purchase_state == "validated":
            users_to_notify = self.partner_id
        else:
            return
        for user in users_to_notify:
            user_name= user.name
            purchase_name = self.name
            if self.purchase_state == "invalidated":
                body_html = f"""
                               <p>Estimado/a {user_name},</p>
                               <p>Los documentos de la compra {purchase_name} estan preparados para ser revisados</p>
                               <p>A continuación, se suministra un enlace directo a la compra:</p>
                               <p><strong>Enlace:</strong> <a href="{purchase_link}">{purchase_name}</a></p>
                               <p>Saludos cordiales, Odoo</p>
                           """
            elif self.purchase_state == "validated":
                body_html = f"""
                               <p>Estimado/a {user_name},</p>
                               <p>Los documentos de la compra {purchase_name} han sido validados</p>
                               <p>A continuación, se suministra un enlace directo a la compra:</p>
                               <p><strong>Enlace:</strong> <a href="{purchase_link}">{purchase_name}</a></p>
                               <p>Saludos cordiales, Odoo</p>
                           """
            email = user.email
            mail_values = {
                'subject': f'Documentos para validar en la compra {purchase_name}',
                'email_from': 'compras@idealfruits.es',
                'email_to': email,
                'body_html': body_html,
            }
            mail = self.env['mail.mail'].create(mail_values)
            mail.send()

    def button_validate_checklist(self):
        for purchase in self:
            if purchase.purchase_state == "need_doc":
                raise ValidationError("No se puede validar la orden de compra, falta documentación.")
            purchase.purchase_state = "validated"
            self._send_mail_checklist()

    def button_invalidate_checklist(self):
        for purchase in self:
            purchase.purchase_state = "invalidated"







