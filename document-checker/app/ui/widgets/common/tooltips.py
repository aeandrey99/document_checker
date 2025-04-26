#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Пакет для управления темой приложения
"""

from theme.styles import apply_theme, configure_tags
from theme.colors import *
from theme.fonts import *

__all__ = [
    'apply_theme', 
    'configure_tags',
    'PRIMARY',
    'PRIMARY_DARK',
    'PRIMARY_LIGHT',
    'BACKGROUND',
    'SURFACE',
    'ERROR',
    'ERROR_LIGHT',
    'WARNING',
    'SUCCESS',
    'SUCCESS_LIGHT',
    'TEXT_PRIMARY',
    'TEXT_SECONDARY',
    'TEXT_DISABLED',
    'TEXT_HINT',
    'BORDER',
    'STATUS_PASSED',
    'STATUS_FAILED',
    'BUTTON_HOVER',
    'FONT_NORMAL',
    'FONT_SMALL',
    'FONT_LARGE',
    'FONT_TITLE',
    'FONT_SMALL_ITALIC',
    'FONT_SMALL_BOLD'
]