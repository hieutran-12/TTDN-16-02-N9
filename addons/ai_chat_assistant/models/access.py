# -*- coding: utf-8 -*-
from odoo import api, models, fields


class IrModelAccess(models.Model):
    _inherit = 'ir.model.access'

    @api.model
    def _auto_init(self):
        """Auto-create access rules for ai_chat_assistant.chat_log"""
        super()._auto_init()
        
        # Get the model
        model = self.env['ir.model'].search([('model', '=', 'ai_chat_assistant.chat_log')], limit=1)
        if not model:
            return
        
        # Get groups
        group_user = self.env.ref('base.group_user', raise_if_not_found=False)
        group_system = self.env.ref('base.group_system', raise_if_not_found=False)
        
        # Create access rules if not exist
        for rule_id, name, group, read, write, create, unlink in [
            ('access_ai_chat_log_user', 'AI Chat Log - User Read', group_user, True, False, False, False),
            ('access_ai_chat_log_admin', 'AI Chat Log - Admin Full', group_system, True, True, True, True),
        ]:
            if group and not self.env['ir.model.access'].search([('name', '=', name)]):
                self.create({
                    'name': name,
                    'model_id': model.id,
                    'group_id': group.id,
                    'perm_read': read,
                    'perm_write': write,
                    'perm_create': create,
                    'perm_unlink': unlink,
                })
