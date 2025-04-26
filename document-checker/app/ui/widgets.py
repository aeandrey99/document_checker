#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import datetime

class UIBuilder:
    """
    Класс для создания и настройки элементов интерфейса приложения.
    """
    def __init__(self, app_instance):
        self.app = app_instance

    def create_widgets(self):
        """
        Создает все элементы интерфейса приложения
        """
        # Верхняя панель (всегда видима)
        self.create_top_panel()
        
        # Панель с кнопками переключения страниц (всегда видима)
        self.create_navigation_panel()
        
        # Создаем контейнер для страницы настроек
        self.settings_page = ttk.Frame(self.app.root)
        self.create_settings_page(self.settings_page)
        
        # Создаем контейнер для страницы статусов и отчётов
        self.status_page = ttk.Frame(self.app.root)
        self.create_status_page(self.status_page)
        
        # Создаем нижнюю панель с информацией о разработчике и датой (всегда видима)
        self.create_bottom_info_panel()
        
        # По умолчанию показываем страницу настроек
        self.show_settings_page()
        
        # Привязываем обработчик событий ко всему дереву один раз
        self.app.results_tree.bind('<Double-1>', self.app.on_item_double_click)
        
        # Настраиваем обработку изменения размера окна
        self.app.root.bind("<Configure>", self.on_window_resize)

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
            command=self.show_settings_page
        )
        self.settings_button.pack(side=tk.LEFT, padx=5)
        
        # Кнопка для перехода на страницу статусов и отчётов
        self.status_button = ttk.Button(
            nav_frame, 
            text="Статус и отчёт", 
            command=self.show_status_page
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

    def create_settings_page(self, parent_frame):
        """
        Создаёт страницу с настройками
        """
        # Создаем все панели настроек внутри контейнера
        self.create_options_panel(parent_frame)
        self.create_search_values_panel(parent_frame)
        self.create_output_panel(parent_frame)

    def create_status_page(self, parent_frame):
        """
        Создаёт страницу со статусами, прогресс-баром и таблицей результатов
        """
        self.create_status_panel(parent_frame)
        self.create_progress_bar(parent_frame)
        self.create_results_table(parent_frame)

    def create_bottom_info_panel(self):
        """Создает нижнюю панель с информацией о разработчике и датой"""
        bottom_info_frame = ttk.Frame(self.app.root, padding="5")
        bottom_info_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        ttk.Label(bottom_info_frame, text="@Собственная разработка ИТРА", 
                font=("", 8, "italic"), foreground="#666666").pack(side=tk.LEFT, padx=10)
        
        current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        ttk.Label(bottom_info_frame, text=f"Текущие дата и время: {current_datetime}", 
                font=("", 8, "italic"), foreground="#666666").pack(side=tk.RIGHT, padx=10)

    def create_top_panel(self):
        """Создает верхнюю панель с выбором пути и кнопкой запуска"""
        top_frame = ttk.Frame(self.app.root, padding="10")
        top_frame.pack(fill=tk.X)
        
        ttk.Label(top_frame, text="Выберите папку или файл:").pack(side=tk.LEFT, padx=(0, 10))
        
        path_entry = ttk.Entry(top_frame, textvariable=self.app.selected_path, width=50)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_button = ttk.Button(top_frame, text="Обзор", command=self.app.browse_path)
        browse_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.app.action_button = ttk.Button(top_frame, text="Начать проверку", command=self.app.start_check)
        self.app.action_button.pack(side=tk.LEFT, padx=(0, 10))

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

    def create_status_panel(self, parent_frame=None):
        """
        Создает панель статуса и текущего файла
        """
        if parent_frame is None:
            parent_frame = self.app.root
            
        status_frame = ttk.Frame(parent_frame, padding="0")
        status_frame.pack(fill=tk.X, pady=0)
        
        ttk.Label(status_frame, text="Статус:").pack(side=tk.LEFT, padx=(0, 5), pady=0)
        ttk.Label(status_frame, textvariable=self.app.status_text).pack(side=tk.LEFT, padx=(0, 20), pady=0)
        
        ttk.Label(status_frame, text="Текущий файл:").pack(side=tk.LEFT, padx=(0, 5), pady=0)
        ttk.Label(status_frame, textvariable=self.app.current_file).pack(side=tk.LEFT, pady=0)

    def create_progress_bar(self, parent_frame=None):
        """
        Создает прогресс-бар и панель с информацией о файлах
        """
        if parent_frame is None:
            parent_frame = self.app.root
            
        progress_frame = ttk.Frame(parent_frame, padding="10")
        progress_frame.pack(fill=tk.X)
        
        self.app.progress_bar = ttk.Progressbar(
            progress_frame, 
            variable=self.app.progress_value,
            length=100,
            mode='determinate'
        )
        self.app.progress_bar.pack(fill=tk.X)
        
        hint_frame = ttk.Frame(parent_frame, padding="2")
        hint_frame.pack(fill=tk.X)
        
        files_count_panel = ttk.Frame(hint_frame)
        files_count_panel.pack(side=tk.LEFT, padx=10)
        
        ttk.Label(files_count_panel, text="Всего файлов для проверки: ").pack(side=tk.LEFT)
        ttk.Label(files_count_panel, textvariable=self.app.total_files_var, font=("", 8, "bold")).pack(side=tk.LEFT)
        
        ttk.Label(files_count_panel, text="    В очереди к проверке: ").pack(side=tk.LEFT)
        ttk.Label(files_count_panel, textvariable=self.app.remaining_files_var, font=("", 8, "bold")).pack(side=tk.LEFT)
        
        ttk.Label(hint_frame, text="Подсказка: дважды щелкните по строке с файлом, чтобы открыть его", 
                font=("", 8, "italic"), foreground="#666666").pack(side=tk.RIGHT, padx=10)

    def create_results_table(self, parent_frame=None):
        """
        Создает таблицу результатов
        """
        if parent_frame is None:
            parent_frame = self.app.root
            
        results_frame = ttk.Frame(parent_frame, padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("№", "Имя файла", "Тип файла", "Путь к файлу", "Результат", "Комментарий")
        self.app.results_tree = ttk.Treeview(results_frame, columns=columns, show='headings')
        
        for col in columns:
            self.app.results_tree.heading(col, text=col)
        
        self.app.results_tree.column("№", width=40, anchor=tk.CENTER)
        self.app.results_tree.column("Имя файла", width=150)
        self.app.results_tree.column("Тип файла", width=80, anchor=tk.CENTER)
        self.app.results_tree.column("Путь к файлу", width=200)
        self.app.results_tree.column("Результат", width=100, anchor=tk.CENTER)
        self.app.results_tree.column("Комментарий", width=300)
        
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.app.results_tree.yview)
        self.app.results_tree.configure(yscroll=scrollbar.set)
        
        self.app.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.app.results_tree.tag_configure('passed', background='#C8E6C9')
        self.app.results_tree.tag_configure('failed', background='#FFCDD2')

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