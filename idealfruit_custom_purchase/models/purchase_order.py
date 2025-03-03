from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def create(self, values):
        record = super(PurchaseOrder, self).create(values)
        record.send_notification_order()
        return record

    def send_notification_order(self):
        purchase_id = str(self.id)
        if "_" in purchase_id:
            purchase_id = purchase_id.split("_")[1]
        purchase_link_base = self.env['ir.config_parameter'].sudo().get_param('notification.base.url')
        if not purchase_link_base:
            raise UserError("No se ha configurado el parámetro del sistema 'notification.base.url'")
        purchase_link = f"{purchase_link_base}/web#id={purchase_id}&cids=1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11%2C12%2C13%2C14%2C15%2C16%2C17%2C18%2C19%2C20%2C21%2C22%2C23%2C24%2C25%2C26%2C27%2C28%2C29%2C30%2C31%2C32%2C33%2C34%2C35%2C36%2C37%2C38%2C39%2C40%2C41%2C42%2C43%2C44%2C45%2C46%2C47%2C48%2C49%2C50%2C51%2C52%2C53%2C54%2C55%2C56%2C57%2C58%2C59%2C60%2C61%2C62%2C63%2C64%2C65%2C66%2C67%2C68%2C69%2C70%2C71%2C72%2C73%2C74%2C75%2C76%2C77%2C78%2C79%2C80%2C81%2C82%2C83%2C84%2C85%2C86%2C87%2C88%2C89%2C90%2C91%2C92%2C93%2C94%2C95%2C96%2C97%2C98%2C99%2C100%2C101%2C102%2C103%2C104%2C105%2C106%2C107%2C108%2C109%2C110%2C111%2C112%2C113%2C114%2C115%2C116%2C117%2C118%2C119%2C120%2C121%2C122%2C123%2C162%2C163%2C164%2C165%2C166%2C167%2C168%2C169%2C170%2C171%2C172%2C173%2C174%2C175%2C176%2C177%2C178%2C179%2C180%2C181%2C182%2C183%2C184%2C185%2C186%2C187%2C188%2C189%2C190%2C191%2C192%2C193&menu_id=245&action=355&model=purchase.order&view_type=form"
        users_to_notify = self.partner_id
        for user in users_to_notify:
            user_name = user.name
            purchase_name = self.name
            body_html = f"""
                              <p>Estimado/a {user_name},</p>
                              <p>Seha generado sele ha asignado una nueva compra: {purchase_name}</p>
                              <p>A continuación, se suministra un enlace directo a la compra:</p>
                              <p><strong>Enlace:</strong> <a href="{purchase_link}">{purchase_name}</a></p>
                              <p>Saludos cordiales, Odoo</p>
                          """
            email = user.email
            mail_values = {
                'subject': f'Nueva compra {purchase_name}',
                'email_from': 'compras@idealfruits.es',
                'email_to': email,
                'body_html': body_html,
            }
            mail = self.env['mail.mail'].create(mail_values)
            mail.send()

    def _get_shipping_address(self,is_company_id=False,partner=False):
        if not partner:
            return
        if is_company_id:
            partner = partner.partner_id
        shipping_addres_partner = partner.child_ids.filtered(lambda r: r.type == 'delivery')
        if shipping_addres_partner:
            return shipping_addres_partner[0]
        return partner


    def _get_fiscal_address(self,is_company_id=False, partner=False):
        if not partner:
            return
        if is_company_id:
            partner = partner.partner_id
        fiscal_address_partner = partner.child_ids.filtered(lambda r: r.type == 'invoice')
        if fiscal_address_partner:
            return fiscal_address_partner[0]
        return partner
