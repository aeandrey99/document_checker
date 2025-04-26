#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль для создания и применения стилей к элементам интерфейса
"""

import tkinter as tk
from tkinter import ttk
from .colors import *
from .fonts import *

def apply_theme(root):
    """
    Применяет единую тему ко всему приложению
    """
    style = ttk.Style()
    
    # Создание базовых стилей
    style.configure(".", 
                    font=FONT_NORMAL,
                    background=BACKGROUND)
    
    # Стили для кнопок
    style.configure("TButton", 
                    font=FONT_NORMAL,
                    background=PRIMARY,
                    foreground=BUTTON_TEXT,  # Используем белый текст для кнопок
                    padding=5)
    
    style.map("TButton", 
              background=[("active", BUTTON_HOVER), ("pressed", PRIMARY_DARK)],
              foreground=[("active", BUTTON_TEXT), ("pressed", BUTTON_TEXT)],  # Белый текст во всех состояниях
              relief=[("pressed", "sunken")])
    
    # Стили для фреймов
    style.configure("TFrame", 
                    background=BACKGROUND)
    
    style.configure("Card.TFrame", 
                    background=SURFACE,
                    relief="raised",
                    borderwidth=1)
    
    # Стили для меток
    style.configure("TLabel", 
                    font=FONT_NORMAL,
                    background=BACKGROUND,
                    foreground=TEXT_PRIMARY)
    
    style.configure("Title.TLabel", 
                    font=FONT_TITLE,
                    foreground=TEXT_PRIMARY)
    
    style.configure("Hint.TLabel", 
                    font=FONT_SMALL_ITALIC,
                    foreground=TEXT_HINT)
    
    style.configure("Small.TLabel", 
                    font=FONT_SMALL,
                    foreground=TEXT_SECONDARY)
    
    # Стили для чекбоксов
    style.configure("TCheckbutton", 
                    font=FONT_NORMAL,
                    background=BACKGROUND)
    
    # Стили для LabelFrame
    style.configure("TLabelframe", 
                    font=FONT_NORMAL,
                    background=BACKGROUND)
    
    style.configure("TLabelframe.Label", 
                    font=FONT_NORMAL,
                    background=BACKGROUND,
                    foreground=TEXT_PRIMARY)
    
    # Стили для Entry
    style.configure("TEntry", 
                    font=FONT_NORMAL,
                    fieldbackground=SURFACE)
    
    # Стили для Notebook (вкладки)
    style.configure("TNotebook", 
                    background=BACKGROUND,
                    tabmargins=[2, 5, 2, 0])
    
    style.configure("TNotebook.Tab", 
                    font=FONT_NORMAL,
                    padding=[10, 2],
                    background=BACKGROUND)
    
    style.map("TNotebook.Tab",
              background=[("selected", SURFACE)],
              expand=[("selected", [1, 1, 1, 0])])
    
    # Стили для прогресс-бара
    style.configure("TProgressbar", 
                    background=PRIMARY,
                    troughcolor=BACKGROUND)
    
    # Стили для Treeview (таблицы)
    style.configure("Treeview", 
                    font=FONT_NORMAL,
                    background=SURFACE,
                    foreground=TEXT_PRIMARY,
                    fieldbackground=SURFACE)
    
    style.configure("Treeview.Heading", 
                    font=FONT_NORMAL,
                    background=BACKGROUND)
    
    style.map("Treeview",
              background=[("selected", PRIMARY_LIGHT)],
              foreground=[("selected", TEXT_PRIMARY)])
    
    # Создаем стиль для иконочных кнопок
    style.configure("Icon.TButton", 
                    font=FONT_NORMAL,
                    padding=3,
                    background=PRIMARY,
                    foreground=BUTTON_TEXT)  # Белый текст для иконочных кнопок
    
    # Стиль для информационной панели
    style.configure("Info.TFrame", 
                    background="#F5F5F5",  # Чуть темнее BACKGROUND для отличия
                    relief="groove",
                    borderwidth=1)
    
    # Дополнительные стили для статусов
    style.configure("Success.TLabel", 
                    foreground=SUCCESS)
    
    style.configure("Error.TLabel", 
                    foreground=ERROR)
    
    # Возвращаем созданный объект стиля
    return style

def configure_tags(tree_widget):
    """
    Настраивает теги для дерева результатов
    """
    tree_widget.tag_configure('passed', background=STATUS_PASSED)
    tree_widget.tag_configure('failed', background=STATUS_FAILED)