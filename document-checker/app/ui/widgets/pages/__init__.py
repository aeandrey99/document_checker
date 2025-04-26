#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Пакет страниц приложения
"""

from .settings_page import SettingsPageBuilder
from .status_page import StatusPageBuilder

__all__ = [
    'SettingsPageBuilder',
    'StatusPageBuilder',
]