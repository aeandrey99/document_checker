#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль для управления шрифтами приложения
"""

# Предпочтительные шрифты (в порядке приоритета)
PREFERRED_FONTS = ["Segoe UI", "Roboto", "Arial", "Helvetica", ""]

# Базовые размеры
SIZE_NORMAL = 10      # Увеличенный с 9 до 10
SIZE_SMALL = 8
SIZE_LARGE = 12
SIZE_TITLE = 11

def get_font_family():
    """
    Возвращает первый доступный шрифт из списка предпочтительных
    
    В реальном приложении здесь должна быть проверка доступности шрифта
    Для демонстрации просто возвращаем первый в списке
    """
    return PREFERRED_FONTS[0]

# Готовые составные шрифты
FONT_NORMAL = (get_font_family(), SIZE_NORMAL)
FONT_SMALL = (get_font_family(), SIZE_SMALL)
FONT_LARGE = (get_font_family(), SIZE_LARGE)
FONT_TITLE = (get_font_family(), SIZE_TITLE, "bold")
FONT_SMALL_ITALIC = (get_font_family(), SIZE_SMALL, "italic")
FONT_SMALL_BOLD = (get_font_family(), SIZE_SMALL, "bold")