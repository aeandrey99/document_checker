#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

class ThemeManager:
    """
    Класс для управления темами приложения
    """
    def __init__(self, app_instance):
        self.app = app_instance
        self.current_theme = "light"  # По умолчанию светлая тема
        
        # Определяем цвета для светлой темы
        self.light_theme = {
            "bg": "#f5f5f5",
            "fg": "#000000",
            "accent": "#4285f4",
            "success": "#34a853",
            "warning": "#fbbc05",
            "error": "#ea4335",
            "selection": "#e6f0ff",
            "panel_bg": "#ffffff",
            "header_bg": "#e0e0e0"
        }
        
        # Определяем цвета для темной темы
        self.dark_theme = {
            "bg": "#222222",
            "fg": "#f0f0f0",
            "accent": "#4285f4",
            "success": "#81c995",
            "warning": "#fdd663",
            "error": "#f28b82",
            "selection": "#3c4043",
            "panel_bg": "#2f2f2f",
            "header_bg": "#1a1a1a"
        }
        
        # Установка темы по умолчанию
        self.current_theme_colors = self.light_theme
        
    def toggle_theme(self):
        """
        Переключает между светлой и темной темами
        """
        if self.current_theme == "light":
            self.current_theme = "dark"
            self.current_theme_colors = self.dark_theme
        else:
            self.current_theme = "light"
            self.current_theme_colors = self.light_theme
            
        self.apply_current_theme()
    
    def apply_current_theme(self):
        """
        Применяет текущую тему к элементам интерфейса
        """
        style = ttk.Style()
        
        # Получаем цвета текущей темы
        colors = self.current_theme_colors
        
        # Настройка базовых стилей
        style.configure('TFrame', background=colors["bg"])
        style.configure('TLabel', background=colors["bg"], foreground=colors["fg"])
        style.configure('TButton', background=colors["bg"], foreground=colors["fg"])
        style.configure('TCheckbutton', background=colors["bg"], foreground=colors["fg"])
        style.configure('TEntry', fieldbackground=colors["panel_bg"], foreground=colors["fg"])
        
        # Настройка специальных элементов
        style.configure('Treeview', background=colors["panel_bg"], foreground=colors["fg"], 
                       fieldbackground=colors["panel_bg"])
        style.map('Treeview', 
                 background=[('selected', colors["accent"])],
                 foreground=[('selected', "#ffffff")])
        
        # Настройка заголовков таблицы
        style.configure('Treeview.Heading', background=colors["header_bg"], foreground=colors["fg"])
        
        # Настройка вкладок
        style.configure('TNotebook', background=colors["bg"])
        style.configure('TNotebook.Tab', background=colors["bg"], foreground=colors["fg"])
        style.map('TNotebook.Tab', 
                 background=[('selected', colors["accent"])],
                 foreground=[('selected', "#ffffff")])
        
        # Настройка прогресс-бара
        style.configure('TProgressbar', 
                       background=colors["accent"],
                       troughcolor=colors["panel_bg"])
        
        # Настройка цветов для результатов в таблице
        if hasattr(self.app, 'results_tree'):
            self.app.results_tree.tag_configure('passed', background=colors["success"] if self.current_theme == "dark" 
                                              else "#C8E6C9")
            self.app.results_tree.tag_configure('failed', background=colors["error"] if self.current_theme == "dark" 
                                              else "#FFCDD2")
        
        # Изменяем фон корневого окна
        self.app.root.configure(background=colors["bg"])
        
        # Обновляем все фреймы, если они существуют
        if hasattr(self.app, 'ui_builder') and hasattr(self.app.ui_builder, 'settings_page'):
            self.app.ui_builder.settings_page.configure(style='TFrame')
            self.app.ui_builder.status_page.configure(style='TFrame')