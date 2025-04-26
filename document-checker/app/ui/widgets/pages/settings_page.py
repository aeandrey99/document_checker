#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from ...theme import TEXT_HINT, FONT_SMALL_ITALIC
from ...widgets.common.tooltips import create_tooltip
from ...widgets.common.utils import UIUtils

class SettingsPageBuilder:
    """
    Класс для создания элементов на странице настроек с улучшенной организацией
    """
    def __init__(self, app_instance):
        self.app = app_instance
        self.utils = UIUtils()

    def create_settings_page(self, parent_frame):
        """
        Создаёт страницу с настройками используя вкладки для логической группировки
        """
        # Создаем блокнот с вкладками
        self.notebook = ttk.Notebook(parent_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Создаем вкладки
        file_types_tab = ttk.Frame(self.notebook, padding=10)
        options_tab = ttk.Frame(self.notebook, padding=10)
        search_tab = ttk.Frame(self.notebook, padding=10)
        output_tab = ttk.Frame(self.notebook, padding=10)
        
        # Добавляем вкладки в блокнот
        self.notebook.add(file_types_tab, text="Типы файлов 📄")
        self.notebook.add(options_tab, text="Опции ⚙")
        self.notebook.add(search_tab, text="Поиск значений 🔍")
        self.notebook.add(output_tab, text="Отчёт 📊")
        
        # Создаем содержимое вкладок
        self._create_file_types_tab(file_types_tab)
        self._create_options_tab(options_tab)
        self._create_search_values_tab(search_tab)
        self._create_output_tab(output_tab)
        
        # Привязываем событие изменения вкладки
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def _create_file_types_tab(self, parent):
        """
        Создает содержимое вкладки с типами файлов
        """
        # Блок с документами Word
        word_frame = ttk.LabelFrame(parent, text="Документы Microsoft Word", padding=10)
        word_frame.pack(fill=tk.X, pady=5)
        
        # Добавляем информационную подсказку
        info_label = ttk.Label(
            word_frame, 
            text="Выберите типы документов Word для проверки:", 
            padding=(0, 0, 0, 5)
        )
        info_label.pack(anchor=tk.W)
        
        # Создаем чекбоксы для форматов Word
        word_checks_frame = ttk.Frame(word_frame)
        word_checks_frame.pack(fill=tk.X)
        
        # Документы DOCX
        docx_check = ttk.Checkbutton(
            word_checks_frame, 
            text=".docx - Документ Word (Office Open XML)", 
            variable=self.app.check_docx
        )
        docx_check.pack(anchor=tk.W, pady=2)
        create_tooltip(docx_check, "Современный формат документов Word (с 2007 года)")
        
        # Документы DOC
        doc_check = ttk.Checkbutton(
            word_checks_frame, 
            text=".doc - Документ Word (Legacy)", 
            variable=self.app.check_doc
        )
        doc_check.pack(anchor=tk.W, pady=2)
        create_tooltip(doc_check, "Устаревший бинарный формат документов Word (до 2007 года)")
        
        # Документы DOCM
        docm_check = ttk.Checkbutton(
            word_checks_frame, 
            text=".docm - Документ Word с макросами", 
            variable=self.app.check_docm
        )
        docm_check.pack(anchor=tk.W, pady=2)
        create_tooltip(docm_check, "Документ Word с поддержкой макросов VBA")
        
        # Блок с таблицами Excel
        excel_frame = ttk.LabelFrame(parent, text="Таблицы Microsoft Excel", padding=10)
        excel_frame.pack(fill=tk.X, pady=10)
        
        # Добавляем информационную подсказку
        info_label = ttk.Label(
            excel_frame, 
            text="Выберите типы таблиц Excel для проверки:", 
            padding=(0, 0, 0, 5)
        )
        info_label.pack(anchor=tk.W)
        
        # Создаем чекбоксы для форматов Excel
        excel_checks_frame = ttk.Frame(excel_frame)
        excel_checks_frame.pack(fill=tk.X)
        
        # Таблицы XLSX
        xlsx_check = ttk.Checkbutton(
            excel_checks_frame, 
            text=".xlsx - Таблица Excel (Office Open XML)", 
            variable=self.app.check_xlsx
        )
        xlsx_check.pack(anchor=tk.W, pady=2)
        create_tooltip(xlsx_check, "Современный формат таблиц Excel (с 2007 года)")
        
        # Таблицы XLS
        xls_check = ttk.Checkbutton(
            excel_checks_frame, 
            text=".xls - Таблица Excel (Legacy)", 
            variable=self.app.check_xls
        )
        xls_check.pack(anchor=tk.W, pady=2)
        create_tooltip(xls_check, "Устаревший бинарный формат таблиц Excel (до 2007 года)")
        
        # Таблицы XLSM
        xlsm_check = ttk.Checkbutton(
            excel_checks_frame, 
            text=".xlsm - Таблица Excel с макросами", 
            variable=self.app.check_xlsm
        )
        xlsm_check.pack(anchor=tk.W, pady=2)
        create_tooltip(xlsm_check, "Таблица Excel с поддержкой макросов VBA")
        
    def _create_options_tab(self, parent):
        """
        Создает содержимое вкладки с дополнительными опциями
        """
        # Рамка с базовыми настройками
        basic_options_frame = ttk.LabelFrame(parent, text="Базовые настройки", padding=10)
        basic_options_frame.pack(fill=tk.X, pady=5)
        
        # Опция пропуска больших файлов
        skip_large_check = ttk.Checkbutton(
            basic_options_frame, 
            text="Пропускать файлы более 100 МБ", 
            variable=self.app.skip_large_files
        )
        skip_large_check.pack(anchor=tk.W, pady=3)
        create_tooltip(skip_large_check, "Большие файлы могут замедлить процесс проверки. Эта опция позволяет их пропускать.")
        
        # Настройки многопоточности
        threads_frame = ttk.Frame(basic_options_frame)
        threads_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(threads_frame, text="Максимальное количество потоков:").pack(side=tk.LEFT, padx=(0, 10))
        
        threads_spinbox = ttk.Spinbox(
            threads_frame, 
            from_=1, 
            to=32, 
            width=5, 
            textvariable=self.app.max_threads
        )
        threads_spinbox.pack(side=tk.LEFT)
        create_tooltip(threads_spinbox, "Больше потоков может ускорить проверку, но увеличит нагрузку на систему")
        
        # Рамка с продвинутыми настройками
        advanced_options_frame = ttk.LabelFrame(parent, text="Продвинутые настройки", padding=10)
        advanced_options_frame.pack(fill=tk.X, pady=10)
        
        # Другие настройки могут быть добавлены здесь
        ttk.Label(
            advanced_options_frame,
            text="Дополнительные настройки появятся в будущих обновлениях",
            font=FONT_SMALL_ITALIC,
            foreground=TEXT_HINT
        ).pack(pady=10)

    def _create_search_values_tab(self, parent):
        """
        Создает содержимое вкладки с настройками поиска значений
        """
        # Рамка с настройками поиска
        search_frame = ttk.LabelFrame(parent, text="Настройки поиска значений", padding=10)
        search_frame.pack(fill=tk.X, pady=5)
        
        # Чекбокс для включения поиска
        enable_search_check = ttk.Checkbutton(
            search_frame,
            text="Включить поиск значений в документах",
            variable=self.app.enable_value_search
        )
        enable_search_check.pack(anchor=tk.W, pady=3)
        create_tooltip(enable_search_check, "Включает поиск указанных значений в содержимом документов")
        
        # Поле для ввода значений поиска
        search_values_frame = ttk.Frame(search_frame)
        search_values_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_values_frame, text="Значения для поиска (через запятую):").pack(anchor=tk.W)
        
        search_entry = ttk.Entry(search_values_frame, textvariable=self.app.search_values, width=50)
        search_entry.pack(fill=tk.X, pady=2)
        create_tooltip(search_entry, "Введите значения для поиска, разделенные запятыми, например: 2024, Предоставлено, Утверждено")
        
        # Чекбокс для учета регистра
        case_sensitive_check = ttk.Checkbutton(
            search_frame,
            text="Учитывать регистр при поиске",
            variable=self.app.case_sensitive
        )
        case_sensitive_check.pack(anchor=tk.W, pady=3)
        create_tooltip(case_sensitive_check, "Если включено, поиск будет чувствителен к регистру символов")
        
        # Информационная подсказка
        ttk.Label(
            search_frame,
            text="Примечание: Поиск значений может замедлить процесс проверки.",
            font=FONT_SMALL_ITALIC,
            foreground=TEXT_HINT
        ).pack(anchor=tk.W, pady=10)
        
    def _create_output_tab(self, parent):
        """
        Создает содержимое вкладки с настройками вывода отчета
        """
        # Рамка выбора пути отчета
        output_frame = ttk.LabelFrame(parent, text="Путь сохранения отчета", padding=10)
        output_frame.pack(fill=tk.X, pady=5)
        
        # Поле ввода пути и кнопка выбора
        path_frame = ttk.Frame(output_frame)
        path_frame.pack(fill=tk.X, pady=5)
        
        # Поле для ввода пути
        output_entry = ttk.Entry(path_frame, textvariable=self.app.output_path, width=50)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        create_tooltip(output_entry, "Укажите путь для сохранения отчета о проверке")
        
        # Кнопка выбора пути
        output_button = ttk.Button(
            path_frame, 
            text="Выбрать 📁", 
            command=self.app.browse_output_path
        )
        output_button.pack(side=tk.LEFT)
        create_tooltip(output_button, "Выбрать папку для сохранения отчета")
        
        # Опции форматирования отчета
        format_frame = ttk.LabelFrame(parent, text="Формат отчета", padding=10)
        format_frame.pack(fill=tk.X, pady=10)
        
        # Опция включения времени в имя файла
        include_time_check = ttk.Checkbutton(
            format_frame, 
            text="Включать время в имя файла отчета", 
            variable=self.app.include_timestamp
        )
        include_time_check.pack(anchor=tk.W, pady=3)
        create_tooltip(include_time_check, "Добавляет время создания в имя файла отчета")
        
        # Другие опции форматирования могут быть добавлены здесь
        ttk.Label(
            format_frame,
            text="Дополнительные опции форматирования появятся в будущих обновлениях",
            font=FONT_SMALL_ITALIC,
            foreground=TEXT_HINT
        ).pack(pady=10)
        
    def _on_tab_changed(self, event):
        """
        Обрабатывает событие изменения активной вкладки
        """
        # Здесь можно добавить специфичную логику при переключении вкладок
        tab_id = self.notebook.index("current")
        tab_text = self.notebook.tab(tab_id, "text")
        
        # Обновляем статусную строку, если она есть
        if hasattr(self.app, 'set_status'):
            self.app.set_status(f"Выбрана вкладка настроек: {tab_text}")