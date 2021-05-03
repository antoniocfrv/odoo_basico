# -*- coding: utf-8 -*-

from odoo import models, fields, api

class pedido (models.Model):
    _name="odoo_basico.pedido" # Será o nome da táboa
    _description = "Modelo pedido"
    _sql_constraints = [('nome_unico', 'unique(name)', 'Non se pode repetir o Identificador')]

    name = fields.Char(required=True, size=20, string="Identificador")
    # para a relación persoa_id propoño duas posibilidades unha na que se usa o campo visible de res_partner que só se pode usar cando usamos o modelo persoa.py
    persoa_id = fields.Many2one('res.partner', ondelete='set null', index=True,string="Persoa")
    #persoa_id = fields.Many2one('res.partner', ondelete='set null', domain="[('visible','=','True')]", index=True,string="Persoa")
    lineapedido_ids = fields.One2many("odoo_basico.lineapedido",'pedido_id') # Os campos One2many Non se almacena na BD

    def actualizadorSexo(self):
        informacion_ids = self.env['odoo_basico.informacion'].search([('autorizado', '=', False)])
        for rexistro in informacion_ids:
            self.env['odoo_basico.informacion']._cambia_campo_sexo(rexistro)

    def actualizadorHoraTimezone(self):
        informacion_ids = self.env['odoo_basico.informacion'].search([])
        for rexistro in informacion_ids:
            self.env['odoo_basico.informacion'].actualiza_hora_timezone_usuario(rexistro)

    def creaRexistroInformacion(self):
        creado_id = self.env['odoo_basico.informacion'].create({'name': 'Creado dende pedido'})
        creado_id.descripcion =  "Creado dende o modelo pedido"
        creado_id.autorizado = False

    def actualizaRexistroInformacion(self):
        informacion_id = self.env['odoo_basico.informacion'].search([('name', '=','Creado dende pedido')])
        if informacion_id:
            informacion_id.name = "Actualizado ..."
            informacion_id.descripcion = "Actualizado dende o modelo pedido"
            informacion_id.sexo_traducido = "Mujer"