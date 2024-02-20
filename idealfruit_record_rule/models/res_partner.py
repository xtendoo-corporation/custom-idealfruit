from odoo import api, models, exceptions


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals):
        # Get the group
        group = self.env.ref('idealfruit_record_rule.idealfruit_group_supplier')

        print("=====================================")
        print("vals: ", vals)
        print("vals['type']: ", vals['type'])
        print("vals['is_company']", vals['is_company'])

        # Check if the current user is in the group
        if vals['is_company'] and group in self.env.user.groups_id:
            raise exceptions.UserError('You are not allowed to create new partners.')

        # If the user is not in the group, proceed with the creation
        return super(ResPartner, self).create(vals)
