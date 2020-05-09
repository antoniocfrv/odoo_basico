# -*- coding: utf-8 -*-

from odoo import models, fields, api

class pedido (models.Model):
    _name="odoo_basico.pedido" # Será o nome da táboa
    _description = "Modelo pedido"
    _sql_constraints = [('nome unico', 'unique(name)', 'Non se pode repetir o Identificador')]

    name = fields.Char(required=True, size=20, string="Identificador")
    persoa_id = fields.Many2one('res.partner', ondelete='set null', domain="[('visible','=','True')]", index=True,string="Persoa")
    lineapedido_ids = fields.One2many("odoo_basico.lineapedido",'pedido_id') # Os campos One2many Non se almacena na BD

    def actualizadorSexo(self):
        informacion_ids = self.env['odoo_basico.informacion'].search([('autorizado', '=', False)])
        for rexistro in informacion_ids:
            self.env['odoo_basico.informacion']._cambia_campo_sexo(rexistro)

    def actualizadorHoraTimezone(self):
        informacion_ids = self.env['odoo_basico.informacion'].search([])
        for rexistro in informacion_ids:
            self.env['odoo_basico.informacion'].actualiza_hora_timezone_usuario(rexistro)
