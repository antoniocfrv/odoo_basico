# -*- coding: utf-8 -*-

import os, platform


def cadeaTextoSegunPlataforma(cadeaTextoWindows,cadeaTextoGNULinux):
    if platform.system().lower() == 'windows':
        cadeaTexto = cadeaTextoWindows
    else:
        cadeaTexto = cadeaTextoGNULinux
    return cadeaTexto

def rexistra_log(diaHora,ruta,arquivo,contido):
    if os.path.exists(ruta):
        # a Ruta ten que existir e previamente terlle concedidos permisos a odoo para poder facer modificacións
        with open(os.path.join(ruta, arquivo), 'a') as ficheiro:
             ficheiro.write(diaHora + " " + contido + cadeaTextoSegunPlataforma('\r\n','\n'))

        # No caso de non ter permisos de escritura no cartafol e se non quixesemos ver o erro por permiso denegado
        # try:
        #     with open(os.path.join(ruta, arquivo), 'a') as ficheiro:
        #         ficheiro.write(diaHora + " " + contido + cadeaTextoSegunPlataforma('\r\n','\n'))
        # except OSError:
        #     pass




