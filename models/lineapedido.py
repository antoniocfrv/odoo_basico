# -*- coding: utf-8 -*-

from odoo import models, fields, api

class lineapedido (models.Model):
    _name="odoo_basico.lineapedido" # Será o nome da táboa
    _description = "Modelo lineapedido"

    descripcion_da_lineapedido = fields.Text(string="A Descripción")
    pedido_id = fields.Many2one('odoo_basico.pedido',ondelete= "cascade",required=True)
    # informacion_ids = fields.Many2many("odoo_basico.informacion")
    # Os campos Many2many crean unha táboa na BD
    informacion_ids = fields.Many2many("odoo_basico.informacion",string="Rexistro de Información",
                                       relation="odoo_basico_lineapedido_informacion",
                                       column1="lineapedido_id",column2="informacion_id",ondelete="set null")
