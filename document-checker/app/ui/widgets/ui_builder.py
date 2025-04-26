#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

from .navigation import NavigationManager
from .settings_page import SettingsPageBuilder
from .status_page import StatusPageBuilder
from .common_panels import PanelsBuilder
from .theme_manager import ThemeManager
from .toolbar import ToolbarBuilder

class UIBuilder:
    """
    Улучшенный класс для создания и настройки элементов интерфейса приложения.
    """
    def __init__(self, app_instance):
        self.app = app_instance
        
        # Инициализируем строителей для разных компонентов
        self.panels_builder = PanelsBuilder(app_instance)
        self.theme_manager = ThemeManager(app_instance)
        self.toolbar_builder = ToolbarBuilder(app_instance)
        self.navigation_manager = NavigationManager(app_instance, self)
        self.settings_builder = SettingsPageBuilder(app_instance)
        self.status_builder = StatusPageBuilder(app_instance)

    def create_widgets(self):
        """
        Создает все элементы интерфейса приложения
        """
        # Применяем тему
        self.theme_manager.apply_current_theme()
        
        # Создаем панель инструментов (новая функция)
        self.toolbar_builder.create_toolbar()
        
        # Верхняя панель (всегда видима)
        self.panels_builder.create_top_panel()
        
        # Создаем вкладки для навигации (вместо кнопок)
        self.notebook = ttk.Notebook(self.app.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Создаем контейнер для страницы настроек
        self.settings_page = ttk.Frame(self.notebook)
        self.settings_builder.create_settings_page(self.settings_page)
        
        # Создаем контейнер для страницы статусов и отчётов
        self.status_page = ttk.Frame(self.notebook)
        self.status_builder.create_status_page(self.status_page)
        
        # Добавляем вкладки
        self.notebook.add(self.settings_page, text="Настройки")
        self.notebook.add(self.status_page, text="Статус и отчёт")
        
        # Создаем статусную строку (новая функция)
        self.create_status_bar()
        
        # Создаем нижнюю панель с информацией о разработчике и датой (всегда видима)
        self.panels_builder.create_bottom_info_panel()
        
        # Привязываем обработчик событий к дереву
        self.app.results_tree.bind('<Double-1>', self.app.on_item_double_click)
        
        # Настраиваем обработку изменения размера окна
        self.app.root.bind("<Configure>", self.on_window_resize)
        
        # Настраиваем контекстное меню
        self.setup_context_menu()
        
        # Привязываем обработчик для обновления статуса
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def create_status_bar(self):
        """
        Создает статусную строку в нижней части интерфейса
        """
        status_bar = ttk.Frame(self.app.root)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Левая часть с информацией о статусе
        status_left = ttk.Frame(status_bar)
        status_left.pack(side=tk.LEFT, fill=tk.X)
        
        ttk.Label(status_left, text="Статус: ").pack(side=tk.LEFT)
        self.app.status_bar_label = ttk.Label(status_left, text="Готов")
        self.app.status_bar_label.pack(side=tk.LEFT)
        
        # Разделитель
        ttk.Separator(status_bar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)
        
        # Правая часть с информацией о файлах
        status_right = ttk.Frame(status_bar)
        status_right.pack(side=tk.RIGHT)
        
        ttk.Label(status_right, text="Файлов обработано: ").pack(side=tk.LEFT)
        self.app.processed_files_label = ttk.Label(status_right, text="0/0")
        self.app.processed_files_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Добавляем переключатель темы
        theme_btn = ttk.Button(status_right, text="Сменить тему", 
                            command=self.theme_manager.toggle_theme, width=12)
        theme_btn.pack(side=tk.RIGHT, padx=5)

    def show_settings_page(self):
        """
        Показывает страницу настроек
        """
        self.notebook.select(0)  # Выбираем первую вкладку (настройки)

    def show_status_page(self):
        """
        Показывает страницу статусов
        """
        self.notebook.select(1)  # Выбираем вторую вкладку (статус)

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
        self.app.context_menu.add_command(label="Копировать строку", command=self.app.copy_row_data)
        self.app.context_menu.add_separator()
        self.app.context_menu.add_command(label="Экспорт результатов", command=self.app.export_results)
        
        self.app.results_tree.bind("<Button-3>", self.app.show_context_menu)
        
    def on_tab_changed(self, event):
        """Обрабатывает переключение вкладок"""
        tab_id = self.notebook.select()
        tab_name = self.notebook.tab(tab_id, "text")
        self.app.status_bar_label.config(text=f"Активная вкладка: {tab_name}")
        
        # Обновление состояния кнопок на панели инструментов
        if tab_name == "Настройки":
            self.toolbar_builder.update_for_settings_page()
        elif tab_name == "Статус и отчёт":
            self.toolbar_builder.update_for_status_page()