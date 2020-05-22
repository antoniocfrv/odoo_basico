# -*- coding: utf-8 -*-

from odoo import models, fields, api

class inicial (models.Model):
    _name="odoo_basico.inicial" # Será o nome da táboa

    name = fields.Char(required=True,size=20,string="Titulo")
