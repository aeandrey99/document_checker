#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

from .navigation import NavigationManager
from .settings_page import SettingsPageBuilder
from .status_page import StatusPageBuilder
from .common_panels import PanelsBuilder

class UIBuilder:
    """
    Класс для создания и настройки элементов интерфейса приложения.
    """
    def __init__(self, app_instance):
        self.app = app_instance
        
        # Инициализируем строителей для разных компонентов
        self.panels_builder = PanelsBuilder(app_instance)
        self.navigation_manager = NavigationManager(app_instance, self)
        self.settings_builder = SettingsPageBuilder(app_instance)
        self.status_builder = StatusPageBuilder(app_instance)

    def create_widgets(self):
        """
        Создает все элементы интерфейса приложения
        """
        # Верхняя панель (всегда видима)
        self.panels_builder.create_top_panel()
        
        # Панель с кнопками переключения страниц (всегда видима)
        self.navigation_manager.create_navigation_panel()
        
        # Создаем контейнер для страницы настроек
        self.settings_page = ttk.Frame(self.app.root)
        self.settings_builder.create_settings_page(self.settings_page)
        
        # Создаем контейнер для страницы статусов и отчётов
        self.status_page = ttk.Frame(self.app.root)
        self.status_builder.create_status_page(self.status_page)
        
        # Создаем нижнюю панель с информацией о разработчике и датой (всегда видима)
        self.panels_builder.create_bottom_info_panel()
        
        # По умолчанию показываем страницу настроек
        self.show_settings_page()
        
        # Привязываем обработчик событий ко всему дереву один раз
        self.app.results_tree.bind('<Double-1>', self.app.on_item_double_click)
        
        # Настраиваем обработку изменения размера окна
        self.app.root.bind("<Configure>", self.on_window_resize)
        
        # Настраиваем контекстное меню
        self.setup_context_menu()

    def show_settings_page(self):
        """
        Показывает страницу настроек и скрывает страницу статусов
        """
        self.status_page.pack_forget()
        self.settings_page.pack(fill=tk.BOTH, expand=True, pady=0)

    def show_status_page(self):
        """
        Показывает страницу статусов и скрывает страницу настроек
        """
        self.settings_page.pack_forget()
        self.status_page.pack(fill=tk.BOTH, expand=True, pady=0)

    def on_window_resize(self, event):
        """Обрабатывает изменение размера окна"""
        if event.widget == self.app.root:
            if hasattr(self.app, 'results_tree'):
                window_width = event.width
                fixed_columns_width = 40 + 150 + 80 + 200 + 100
                scrollbar_width = 20
                padding = 40
                available_width = max(200, window_width - fixed_columns_width - scrollbar_width - padding)
                self.app.results_tree.column("Комментарий", width=available_width)

    def setup_context_menu(self):
        """Настраивает контекстное меню для таблицы результатов"""
        self.app.context_menu = tk.Menu(self.app.root, tearoff=0)
        self.app.context_menu.add_command(label="Открыть файл", command=self.app.open_selected_file)
        self.app.context_menu.add_command(label="Открыть директорию файла", command=self.app.open_file_directory)
        self.app.context_menu.add_separator()
        self.app.context_menu.add_command(label="Копировать путь", command=self.app.copy_file_path)
        
        self.app.results_tree.bind("<Button-3>", self.app.show_context_menu)