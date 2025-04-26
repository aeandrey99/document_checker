#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Пакет пользовательского интерфейса приложения
"""

from .widgets import UIBuilder
from .theme import apply_theme, configure_tags

__all__ = [
    'UIBuilder',
    'apply_theme',
    'configure_tags'
]