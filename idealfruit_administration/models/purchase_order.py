from odoo import models, api, fields

class PurchaseOrder(models.Model):
    _inherit = ['purchase.order', 'mixin.rule']
    _name="purchase.order"

class PurchaseOrderLine(models.Model):
    _inherit = ['purchase.order.line', 'mixin.rule']
    _name = "purchase.order.line"

    # is_not_create_group = fields.Boolean("is_not_create_group", compute='_compute_is_not_create_group', default=lambda self: self._get_default_is_not_create_group())


    # def _compute_is_not_create_group(self):
    #     for record in self:
    #         user_groups = self.env.user.groups_id
    #         group_not_create = self.env.ref('idealfruit_administration.group_not_create')
    #         print("*" * 100)
    #         print(user_groups)
    #         print(group_not_create)
    #         print("*" * 100)
    #         record.is_not_create_group = group_not_create in user_groups
    #
    # def _get_default_is_not_create_group(self):
    #     return False
    #     # user_groups = self.env.user.groups_id
    #     # group_not_create = self.env.ref('idealfruit_administration.group_not_create')
    #     # print("*"*100)
    #     # print(group_not_create)
    #     # print("*"*100)
    #     # return group_not_create in user_groups

