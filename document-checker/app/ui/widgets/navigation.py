#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

class NavigationManager:
    """
    Класс для управления навигацией между страницами приложения
    """
    def __init__(self, app_instance, ui_builder):
        self.app = app_instance
        self.ui_builder = ui_builder

    def create_navigation_panel(self):
        """
        Создает панель с кнопками для переключения между страницами
        """
        nav_frame = ttk.Frame(self.app.root)
        nav_frame.pack(fill=tk.X, padx=5, pady=0)
        
        # Кнопка для перехода на страницу настроек
        self.settings_button = ttk.Button(
            nav_frame, 
            text="Настройки", 
            command=self.ui_builder.show_settings_page
        )
        self.settings_button.pack(side=tk.LEFT, padx=5)
        
        # Кнопка для перехода на страницу статусов и отчётов
        self.status_button = ttk.Button(
            nav_frame, 
            text="Статус и отчёт", 
            command=self.ui_builder.show_status_page
        )
        self.status_button.pack(side=tk.LEFT, padx=5)
        
        # Информация о текущем запуске (справа)
        info_frame = ttk.Frame(nav_frame)
        info_frame.pack(side=tk.RIGHT, padx=10)
        
        ttk.Label(info_frame, text="Текущий номер запуска: ", 
                font=("", 8)).pack(side=tk.LEFT)
        self.app.run_id_label = ttk.Label(info_frame, text=str(self.app.report_manager.current_run_id), 
                font=("", 8, "bold"))
        self.app.run_id_label.pack(side=tk.LEFT)