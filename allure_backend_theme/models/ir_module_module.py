# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

import base64
from odoo import api, fields, models, modules, tools

class IrModule(models.Model):
    _inherit = 'ir.module.module'

    icon = fields.Char('Icon URL')
    theme_icon = fields.Char('Theme Icon URL', readonly=True, index=True)

    def button_uninstall(self):
        url = '/allure_backend_theme/static/src/scss/variables.scss'
        self.env['web_editor.assets'].reset_asset(url, 'web.assets_backend')
        return super(IrModule, self).button_uninstall()

    @api.depends('icon')
    def _get_icon_image(self):
        for module in self:
            module.icon_image = ''
            if module.theme_icon:
                path_parts = module.theme_icon.split('/')
                path = modules.get_module_resource(path_parts[1], *path_parts[2:])
            else:
                icon_path = modules.module.get_module_icon(module.name)
                icon_path = icon_path.split('/')
                path = modules.get_module_resource(icon_path[1], *icon_path[2:])
            if not path:
                path = 'allure_backend_theme/static/src/img/no_modul_ioc.png'
            if path:
                with tools.file_open(path, 'rb') as image_file:
                    module.icon_image = base64.b64encode(image_file.read())
