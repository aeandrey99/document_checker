#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import datetime
from ...theme import FONT_SMALL_ITALIC, TEXT_HINT
from .tooltips import create_tooltip
from .utils import UIUtils

class PanelsBuilder:
    """
    Класс для создания общих панелей интерфейса
    """
    def __init__(self, app_instance):
        self.app = app_instance
        self.status_var = tk.StringVar()
        self.utils = UIUtils()

    def create_top_panel(self):
        """Создает верхнюю панель с выбором пути и кнопкой запуска"""
        top_frame = ttk.Frame(self.app.root, padding="15")
        top_frame.pack(fill=tk.X)
        
        ttk.Label(top_frame, text="Выберите папку или файл:").pack(side=tk.LEFT, padx=(0, 10))
        
        # Создаем рамку для поля ввода и кнопки обзора
        path_frame = ttk.Frame(top_frame)
        path_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))
        
        # Поле для ввода пути
        self.path_entry = ttk.Entry(path_frame, textvariable=self.app.selected_path, width=50)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        create_tooltip(self.path_entry, "Полный путь к папке или файлу для проверки")
        
        # Кнопка обзора с иконкой
        browse_button = ttk.Button(
            top_frame, 
            text="Обзор 🗂", 
            command=self.app.browse_path
        )
        browse_button.pack(side=tk.LEFT, padx=(0, 15))
        
        create_tooltip(browse_button, "Выбрать папку или файл для проверки")
        
        # Кнопка запуска с иконкой
        self.app.action_button = ttk.Button(
            top_frame, 
            text="Начать проверку ▶", 
            command=self.start_check_with_confirm
        )
        self.app.action_button.pack(side=tk.LEFT)
        
        create_tooltip(self.app.action_button, "Запустить процесс проверки выбранных файлов")

    def start_check_with_confirm(self):
        """
        Запускает проверку с подтверждением пользователя
        если выбрано много файлов или включены ресурсоемкие опции
        """
        # Проверяем, сколько файлов выбрано
        file_count = self.app.get_file_count() if hasattr(self.app, 'get_file_count') else 0
        value_search_enabled = self.app.enable_value_search.get() if hasattr(self.app, 'enable_value_search') else False
        
        # Если выбрано много файлов или включен поиск значений
        if file_count > 20 or value_search_enabled:
            message = ""
            if file_count > 20:
                message += f"Выбрано {file_count} файлов. "
            if value_search_enabled:
                message += "Включен поиск значений, что может замедлить проверку. "
            message += "Начать проверку?"
            
            if UIUtils.ask_confirm("Подтверждение", message):
                self.app.start_check()
        else:
            # Если файлов немного и не включены ресурсоемкие опции, запускаем без подтверждения
            self.app.start_check()

    def create_bottom_info_panel(self):
        """Создает нижнюю панель с информацией о разработчике и датой"""
        bottom_info_frame = ttk.Frame(self.app.root, padding="5", style="Info.TFrame")
        bottom_info_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Добавляем логотип или иконку компании (если есть)
        company_frame = ttk.Frame(bottom_info_frame)
        company_frame.pack(side=tk.LEFT, padx=10)
        
        # Информация о разработчике
        ttk.Label(
            company_frame, 
            text="@Собственная разработка ИТРА", 
            font=FONT_SMALL_ITALIC, 
            foreground=TEXT_HINT
        ).pack(side=tk.LEFT)
        
        # Текущая дата и время с обновлением
        self.datetime_label = ttk.Label(
            bottom_info_frame, 
            font=FONT_SMALL_ITALIC, 
            foreground=TEXT_HINT
        )
        self.datetime_label.pack(side=tk.RIGHT, padx=10)
        
        # Обновление времени при инициализации
        self.update_datetime()
        
    def update_datetime(self):
        """Обновляет отображение текущей даты и времени"""
        current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.datetime_label.config(text=f"Текущие дата и время: {current_datetime}")
        
        # Планируем следующее обновление через 1 секунду
        self.app.root.after(1000, self.update_datetime)
        
    def create_status_bar(self):
        """
        Создает статусную строку, которая показывает контекстную информацию
        """
        status_bar = ttk.Frame(self.app.root)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)  # Removed 'before' option
        
        # Левая часть - системные сообщения
        self.status_label = ttk.Label(
            status_bar, 
            textvariable=self.status_var,
            foreground=TEXT_HINT,
            font=FONT_SMALL_ITALIC
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Правая часть - счетчик проверенных файлов
        self.file_counter_frame = ttk.Frame(status_bar)
        self.file_counter_frame.pack(side=tk.RIGHT, padx=10)
        
        # Устанавливаем начальное сообщение
        self.set_status("Готово к работе. Выберите папку или файл для проверки.")
        
    def set_status(self, text):
        """
        Устанавливает текст в статусной строке
        """
        self.status_var.set(text)