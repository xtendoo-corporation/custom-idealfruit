from odoo import models, fields, api
import base64
from datetime import datetime
import os
from odoo.exceptions import UserError

class PurchaseLineIndications(models.Model):
    _name = 'purchase.line.indications'
    _description = 'Purchase Line Indications'

    purchase_line_id = fields.Many2one(
        'purchase.order.line', string='Purchase Order Line', required=True
    )
    indications = fields.Text(string='Indicaciones')
    indications_attachment_temp=fields.Binary(string="Subir adjunto")
    indications_filename = fields.Char(string="Nombre del archivo")
    indications_attachment_id = fields.Many2one(
        'ir.attachment',
        string='Adjunto',
        help='Archivo adjunto relacionado a la indicación'
    )

    def create(self, vals):
        current_date = fields.Datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        for val in vals:
            if 'indications_attachment_temp' in val and 'indications_filename' in val:
                filename = val['indications_filename']
                if filename:
                    file_extension = os.path.splitext(filename)[1]
                    if file_extension not in ['.jpg', '.png', '.pdf']:
                        raise UserError("Extensión no permitida")
                    filename = f"{filename}_{current_date}{file_extension}"
                    val['indications_filename'] = filename
                    attachment = self.env['ir.attachment'].create({
                                'name': filename,
                                'type': 'binary',
                                'datas': val['indications_attachment_temp'],
                                'res_model': 'purchase.line.indications',
                            })
                    val['indications_attachment_id'] = attachment.id  # Asocia el adjunto al campo 'indications_attachment_id'

        return super().create(vals)

    def action_open_attachment(self):
        self.ensure_one()
        if self.indications_attachment_id:
            return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{self.indications_attachment_id.id}?download=false',
                'target': 'new',
            }
