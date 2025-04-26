#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

class SettingsPageBuilder:
    """
    Класс для создания элементов на странице настроек
    """
    def __init__(self, app_instance):
        self.app = app_instance

    def create_settings_page(self, parent_frame):
        """
        Создаёт страницу с настройками
        """
        # Создаем все панели настроек внутри контейнера
        self.create_options_panel(parent_frame)
        self.create_search_values_panel(parent_frame)
        self.create_output_panel(parent_frame)
        
    def create_options_panel(self, parent_frame=None):
        """
        Создает панель с настройками типов файлов и дополнительными опциями
        """
        if parent_frame is None:
            parent_frame = self.app.root
            
        options_panel = ttk.Frame(parent_frame, padding="5")
        options_panel.pack(fill=tk.X, padx=5, pady=2)
        
        file_types_frame = ttk.LabelFrame(options_panel, text="Типы файлов для проверки", padding="5")
        file_types_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        word_frame = ttk.Frame(file_types_frame)
        word_frame.pack(fill=tk.X, pady=2)
        ttk.Label(word_frame, text="Word:", width=8).pack(side=tk.LEFT)
        ttk.Checkbutton(word_frame, text=".docx", variable=self.app.check_docx).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(word_frame, text=".doc", variable=self.app.check_doc).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(word_frame, text=".docm", variable=self.app.check_docm).pack(side=tk.LEFT, padx=5)
        
        excel_frame = ttk.Frame(file_types_frame)
        excel_frame.pack(fill=tk.X, pady=2)
        ttk.Label(excel_frame, text="Excel:", width=8).pack(side=tk.LEFT)
        ttk.Checkbutton(excel_frame, text=".xlsx", variable=self.app.check_xlsx).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(excel_frame, text=".xls", variable=self.app.check_xls).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(excel_frame, text=".xlsm", variable=self.app.check_xlsm).pack(side=tk.LEFT, padx=5)
        
        add_options_frame = ttk.LabelFrame(options_panel, text="Дополнительные опции", padding="5")
        add_options_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        ttk.Checkbutton(add_options_frame, text="Пропускать файлы более 100 МБ", 
                        variable=self.app.skip_large_files).pack(anchor=tk.W)
        
        threads_frame = ttk.Frame(add_options_frame)
        threads_frame.pack(anchor=tk.W, pady=2)
        
        ttk.Label(threads_frame, text="Макс. количество потоков: ").pack(side=tk.LEFT)
        
        threads_spinbox = ttk.Spinbox(threads_frame, from_=1, to=32, width=5, 
                                    textvariable=self.app.max_threads)
        threads_spinbox.pack(side=tk.LEFT)

    def create_search_values_panel(self, parent_frame=None):
        """
        Создает панель для поиска заданных пользователем значений
        """
        if parent_frame is None:
            parent_frame = self.app.root
            
        search_frame = ttk.LabelFrame(parent_frame, text="Поиск значений в документах", padding="10")
        search_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Checkbutton(search_frame, text="Дополнительный поиск значений", 
                        variable=self.app.enable_value_search).pack(anchor=tk.W)
        
        values_frame = ttk.Frame(search_frame)
        values_frame.pack(fill=tk.X, pady=5)
        
        values_entry = ttk.Entry(values_frame, textvariable=self.app.search_values, width=80)
        values_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        hint_text = ("Укажите значения для поиска в формате: \"2024\", \"Привет_\", \"Предоставлено \", ...\n"
                     "Значения должны быть заключены в двойные кавычки и разделены запятыми. "
                     "Пробелы и другие символы учитываются.")
        ttk.Label(search_frame, text=hint_text, 
                 font=("", 8, "italic"), foreground="#666666").pack(anchor=tk.W, pady=2)

    def create_output_panel(self, parent_frame=None):
        """
        Создает панель выбора пути для отчета
        """
        if parent_frame is None:
            parent_frame = self.app.root
            
        output_frame = ttk.Frame(parent_frame, padding="5")
        output_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(output_frame, text="Путь сохранения отчета:").pack(side=tk.LEFT, padx=(0, 10))
        
        output_entry = ttk.Entry(output_frame, textvariable=self.app.output_path, width=50)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        output_button = ttk.Button(output_frame, text="Выбрать", command=self.app.browse_output_path)
        output_button.pack(side=tk.LEFT)