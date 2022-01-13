# -*- coding: utf-8 -*-

import os, platform


def idiomaSegunPlataforma(idiomaWindows,idiomaGNULinux):
    if platform.system().lower() == 'windows':
        idioma = idiomaWindows
    else:
        idioma = idiomaGNULinux
    return idioma