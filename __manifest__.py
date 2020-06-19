# -*- coding: utf-8 -*-
{
    'name': "odoo_basico",

    'summary': """
        Exemplos dos tipos de datos a utilizar """,

    'description': """
       Exemplos dos tipos de datos a utilizar e vistas,menús....
    """,

    'author': "Antonio",
    'website': "https://www.edu.xunta.gal/centros/iesteis/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','account'],

    # always loaded
    'data': [
        'accions_planificadas/accion_planificada.xml',
        'views/inicial.xml',
        'views/suceso.xml',
        #'views/persoa.xml',
        'views/informacion.xml',
        'views/pedido.xml',
        'views/lineapedido.xml',
        'views/templates.xml',
        'reports/report_header.xml',
        'reports/report_informacion.xml',
        'views/menu.xml',
        #'security/xestion_usuarios.xml', #comentar e descomentar en función VersiónBasica ou VersionXestion_usuarios
        # versionXestion_usuarios:Para xestionar que os usuarios teñan os permisos por grupos (escritura,lectura)
        # Copiar ir.model.accessVersionXestion_usuarios como ir.model.access.csv e actualizar o módulo
        'security/ir.model.access.csv',
        # versionBasica: Para xestionar que todos os usuarios teñan todos os permisos
        # Copiar ir.model.accessVersionBasica como ir.model.access.csv e actualizar o módulo
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license' : 'AGPL-3',
    'installable': True,
    'application': True,
}