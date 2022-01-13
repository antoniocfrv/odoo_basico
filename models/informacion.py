# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.exceptions import Warning
import pytz
import locale
import os
from . import miñasUtilidades

class informacion (models.Model):
    _name="odoo_basico.informacion" # Será o nome da táboa
    _description = "Tipos de datos básicos"
    _order = "descripcion desc"
    _sql_constraints = [('nome_unico', 'unique(name)', 'Non se pode repetir o nome')]

    name = fields.Char(required=True,size=20,string="Titulo")
    descripcion = fields.Text(string="A Descripción")# string é a etiqueta do campo
    autorizado = fields.Boolean(string="¿Autorizado?", default=True)
    sexo_traducido = fields.Selection([('Hombre', 'Home'), ('Mujer', 'Muller'), ('Otros', 'Outros')], string='Sexo')
    data = fields.Date(string="Data", default=lambda self: fields.Date.today())
    data_hora = fields.Datetime(string="Data e Hora", default=lambda self: fields.Datetime.now())
    mes_castelan = fields.Char(compute="_mes_castelan", size=15,string="Mes castelán", store=True)
    mes_galego = fields.Char(compute="_mes_galego", size=15, store=True)
    hora_utc  = fields.Char(compute="_hora_utc",string="Hora UTC", size=15, store=True)
    hora_timezone_usuario  = fields.Char(compute="_hora_timezone_usuario",string="Hora Timezone do Usuario", size=15, store=True)
    hora_actual  = fields.Char(compute="_hora_actual",string="Hora Actual", size=15, store=True)
    alto_en_cms = fields.Integer(string="Alto en centímetros")
    longo_en_cms = fields.Integer(string="Longo en centímetros")
    ancho_en_cms = fields.Integer(string="Ancho en centímetros")
    volume = fields.Float(compute="_volume", store=True)
    volume_entre_100 = fields.Float(compute="_volume_entre_100", store=False)
    peso = fields.Float(digits=(6, 2), string="Peso en Kg.s", default=2.7)
    densidade = fields.Float(compute="_densidade", store=True)
    # Os campos Many2one crean un campo na BD
    moeda_id = fields.Many2one('res.currency',domain="[('position','=','after')]") 
    # con domain, filtramos os valores mostrados. Pode ser mediante unha constante (vai entre comillas) ou unha variable
    gasto = fields.Monetary("Gasto", 'moeda_id')
    foto = fields.Binary(string="Foto")
    nome_adxunto = fields.Char(size=20, string="Nome Adxunto")
    adxunto = fields.Binary(string="Arquivo Adxunto")

    moeda_euro_id = fields.Many2one('res.currency',
                                    default=lambda self: self.env['res.currency'].search([('name', '=', "EUR")],
                                                                                         limit=1))
    gasto_en_euros = fields.Monetary("Gasto en Euros", 'moeda_euro_id')
    moeda_en_texto = fields.Char(related="moeda_id.currency_unit_label", string="Moeda en formato texto",store=True)
    creador_da_moeda = fields.Char(related="moeda_id.create_uid.login", string="Usuario creador da moeda", store=True)


    @api.depends('alto_en_cms', 'longo_en_cms', 'ancho_en_cms')
    def _volume(self):
        for rexistro in self:
            rexistro.volume = float(rexistro.alto_en_cms) * float(rexistro.longo_en_cms) * float(rexistro.ancho_en_cms)
            miñasUtilidades.rexistra_log(self.convirte_data_hora_de_utc_a_timezone_do_usuario(fields.Datetime.now()).strftime("%Y/%m/%d, %H:%M:%S"),
                                         miñasUtilidades.cadeaTextoSegunPlataforma('c:\\users\antonio\logs', '/home/antonio/logs'),
                                         "probaVolume.log", "novo volume " + str(rexistro.volume))

    @api.depends('alto_en_cms', 'longo_en_cms', 'ancho_en_cms')
    def _volume_entre_100(self):
        for rexistro in self:
            rexistro.volume_entre_100 = (float(rexistro.alto_en_cms) * float(rexistro.longo_en_cms) * float(rexistro.ancho_en_cms))/100

    @api.depends('volume', 'peso')
    def _densidade(self):
        for rexistro in self:
            if rexistro.volume !=0:
                rexistro.densidade = 100 * (float(rexistro.peso) / float(rexistro.volume))
            else:
                rexistro.densidade = 0

    @api.constrains('peso')  # Ao usar ValidationError temos que importar a libreria ValidationError
    def _constrain_peso(self):   # from odoo.exceptions import ValidationError
        for rexistro in self:
            if rexistro.peso < 1 or rexistro.peso > 4:
                raise ValidationError('Os peso de %s ten que ser entre 1 e 4 ' % rexistro.name)

    # Podemos  configurar locales a nivel de sistema con dpkg-reconfigure locales poñendo un por defecto.
    # apt-get install locales
    # dpkg-reconfigure locales (podemos configurar varios)
    # locale (ver o locale por defecto)
    # locale -a (ver os dispoñibles)

    @api.depends('data_hora')
    def _mes_castelan(self):
        # O idioma por defecto é o configurado en locale na máquina onde se executa odoo.
        # Podemos cambialo con locale.setlocale, os idiomas teñen que estar instalados na máquina onde se executa odoo.
        # Lista onde podemos ver os distintos valores: https://docs.moodle.org/dev/Table_of_locales#Table
        # Definimos en miñasUtilidades un método para asignar o distinto literal que ten o idioma en función da plataforma Windows ou GNULinux
        locale.setlocale(locale.LC_TIME, miñasUtilidades.cadeaTextoSegunPlataforma('Spanish_Spain.1252','es_ES.utf8'))
        for rexistro in self:
            rexistro.mes_castelan = rexistro.data_hora.strftime("%B") # strftime https://strftime.org/

    @api.depends('data_hora')
    def _mes_galego(self):
        # O idioma por defecto é o configurado en locale na máquina onde se executa odoo.
        # Podemos cambialo con locale.setlocale, os idiomas teñen que estar instalados na máquina onde se executa odoo.
        # Lista onde podemos ver os distintos valores: https://docs.moodle.org/dev/Table_of_locales#Table
        # Definimos en miñasUtilidades un método para asignar o distinto literal que ten o idioma en función da plataforma Windows ou GNULinux
        locale.setlocale(locale.LC_TIME, miñasUtilidades.cadeaTextoSegunPlataforma('Galician_Spain.1252', 'gl_ES.utf8'))
        for rexistro in self:
            rexistro.mes_galego = rexistro.data_hora.strftime("%B")
        locale.setlocale(locale.LC_TIME, miñasUtilidades.cadeaTextoSegunPlataforma('Spanish_Spain.1252', 'es_ES.utf8'))

    @api.depends('data_hora')
    def _hora_utc(self):
        for rexistro in self: # A hora se almacena na BD en horario UTC (2 horas menos no verán, 1 hora menos no inverno)
            rexistro.hora_utc = rexistro.data_hora.strftime("%H:%M:%S")

    def convirte_data_hora_de_utc_a_timezone_do_usuario(self,data_hora_utc_object):  # recibe a data hora en formato object
        usuario_timezone = pytz.timezone(self.env.user.tz or 'UTC')  # obter a zona horaria do usuario. Ollo!!! nas preferencias do usuario ten que estar ben configurada a zona horaria
        return pytz.UTC.localize(data_hora_utc_object).astimezone(usuario_timezone)  # hora co horario do usuario en formato object
        # para usar  pytz temos que facer  import pytz


    # Engadimos nas vistas  buttons no header. O name do button é o nome da función

    # Esta función será chamada dende a función actualiza_hora_timezone_usuario_dende_boton_e_apidepends e
    #  dende pedido.py (Cando insertamos os valores do template self.env.user.tz non ten o timezone do usuario por iso se carga coa hora UTC,
    #  o botón en pedido.py é para actualizar todos os rexistros masivamente dende outro modelo)
    def actualiza_hora_timezone_usuario(self,obxeto_rexistro):
        obxeto_rexistro.hora_timezone_usuario = self.convirte_data_hora_de_utc_a_timezone_do_usuario(obxeto_rexistro.data_hora).strftime("%H:%M:%S") # Convertimos a hora de UTC a hora do timezone do usuario

    def actualiza_hora_timezone_usuario_dende_boton_e_apidepends(self):# Esta función é chamada dende un boton de informacion.xml e dende @api.depends _hora_timezone_usuario
        self.actualiza_hora_timezone_usuario(self)  # leva self como parametro por que actualiza_hora_timezone_usuario ten 2 parametros
        # porque usamos tamén actualiza_hora_timezone_usuario dende outro modelo (pedido.py) e lle pasamos como parámetro o obxeto_rexistro

    @api.depends('data_hora')
    def _hora_timezone_usuario(self):
        for rexistro in self:
            rexistro.actualiza_hora_timezone_usuario_dende_boton_e_apidepends()

    def actualiza_hora_actual_UTC(self): # Esta función é chamada dende un boton de informacion.xml e dende _hora_actual
        for rexistro in self:
            rexistro.hora_actual = fields.Datetime.now().strftime("%H:%M:%S")
        # Grava a hora en UTC, se quixesemos poderiamos usar a función  _convirte_data_hora_de_utc_a_timezone_do_usuario

    @api.depends('data_hora')
    def _hora_actual(self):
        for rexistro in self:
            rexistro.actualiza_hora_actual_UTC()

    def ver_contexto(self): # Este método é chamado dende un botón de informacion.xml
        for rexistro in self:
            #Ao usar warning temos que importar a libreria mediante from odoo.exceptions import Warning
            #Importamos tamén a libreria os mediante import os
            raise Warning('Contexto: %s Ruta: %s Contido %s' % (rexistro.env.context, os.getcwd(),os.listdir(os.getcwd())))
            #env.context é un diccionario  https://www.w3schools.com/python/python_dictionaries.asp
        return True

    def _cambia_campo_sexo(self, rexistro):
        rexistro.sexo_traducido = "Hombre"

    def envio_email(self):
        meu_usuario = self.env.user
        #mail_de     Odoo pon o email que configuramos en gmail para facer o envio
        mail_reply_to = meu_usuario.partner_id.email  # o enderezo email que ten asociado o noso usuario
        mail_para = 'emaildedestino@servidordedestino.com'  # o enderezo email de destino
        mail_valores = {
            'subject': 'Aquí iría o asunto do email ',
            'author_id': meu_usuario.id,
            'email_from': mail_reply_to,
            'email_to': mail_para,
            'message_type': 'email',
            'body_html': 'Aquí iría o corpo do email cos datos por exemplo de "%s" ' % self.descripcion,
        }
        mail_id = self.env['mail.mail'].create(mail_valores)
        mail_id.sudo().send()
        return True

    def literal_informativo_da_hora(self): # Esta función é chamada dende un boton de informacion.xml
        data_hora_timezone_usuario_object = self.convirte_data_hora_de_utc_a_timezone_do_usuario(fields.Datetime.now())
        for rexistro in self:
            data_hora_do_campo_da_bd = self.convirte_data_hora_de_utc_a_timezone_do_usuario(rexistro.data_hora)
            raise Warning('Datetime.now() devolve a hora UTC %s cambiamola coa configuración horaria do usuario %s cambiamos tamén a do campo data_hora %s'
                       % (fields.Datetime.now().strftime ('%Y-%m-%d %H:%M'),data_hora_timezone_usuario_object,data_hora_do_campo_da_bd))
        return True