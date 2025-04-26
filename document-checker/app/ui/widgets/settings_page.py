#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

class SettingsPageBuilder:
    """
    Улучшенный класс для создания элементов на странице настроек
    """
    def __init__(self, app_instance):
        self.app = app_instance

    def create_settings_page(self, parent_frame):
        """
        Создаёт улучшенную страницу с настройками, разделенную на логические блоки
        """
        # Создаем фрейм с прокруткой для размещения всех панелей
        canvas = tk.Canvas(parent_frame)
        scrollbar = ttk.Scrollbar(parent_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Обрабатываем прокрутку колесом мыши
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        # Создаем все панели настроек внутри прокручиваемого контейнера
        self.create_file_types_panel(scrollable_frame)
        self.create_advanced_options_panel(scrollable_frame)
        self.create_search_values_panel(scrollable_frame)
        self.create_output_panel(scrollable_frame)
        self.create_presets_panel(scrollable_frame)
        
    def create_file_types_panel(self, parent_frame):
        """
        Создает улучшенную панель с настройками типов файлов
        """
        file_types_frame = ttk.LabelFrame(parent_frame, text="Типы файлов для проверки", padding="10")
        file_types_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Добавляем кнопки быстрого выбора
        quick_select_frame = ttk.Frame(file_types_frame)
        quick_select_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(quick_select_frame, text="Выбрать все", 
                 command=self.select_all_file_types, width=15).pack(side=tk.LEFT, padx=5)
                 
        ttk.Button(quick_select_frame, text="Снять все", 
                 command=self.deselect_all_file_types, width=15).pack(side=tk.LEFT, padx=5)
                 
        ttk.Button(quick_select_frame, text="Только Word", 
                 command=self.select_only_word, width=15).pack(side=tk.LEFT, padx=5)
                 
        ttk.Button(quick_select_frame, text="Только Excel", 
                 command=self.select_only_excel, width=15).pack(side=tk.LEFT, padx=5)
        
        # Создаем группы флажков
        file_types_container = ttk.Frame(file_types_frame)
        file_types_container.pack(fill=tk.X)
        
        # Word документы
        word_frame = ttk.LabelFrame(file_types_container, text="Microsoft Word", padding="5")
        word_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Checkbutton(word_frame, text=".docx - Office Open XML Document", 
                      variable=self.app.check_docx).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(word_frame, text=".doc - Бинарный формат документа", 
                      variable=self.app.check_doc).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(word_frame, text=".docm - Документ с макросами", 
                      variable=self.app.check_docm).pack(anchor=tk.W, pady=2)
        
        # Excel документы
        excel_frame = ttk.LabelFrame(file_types_container, text="Microsoft Excel", padding="5")
        excel_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        ttk.Checkbutton(excel_frame, text=".xlsx - Office Open XML Таблица", 
                      variable=self.app.check_xlsx).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(excel_frame, text=".xls - Бинарный формат таблицы", 
                      variable=self.app.check_xls).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(excel_frame, text=".xlsm - Таблица с макросами", 
                      variable=self.app.check_xlsm).pack(anchor=tk.W, pady=2)

    def create_advanced_options_panel(self, parent_frame):
        """
        Создает улучшенную панель с расширенными настройками
        """
        advanced_frame = ttk.LabelFrame(parent_frame, text="Расширенные настройки", padding="10")
        advanced_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Левая колонка
        left_column = ttk.Frame(advanced_frame)
        left_column.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Настройки размера файлов
        size_frame = ttk.Frame(left_column)
        size_frame.pack(fill=tk.X, pady=2)
        
        ttk.Checkbutton(size_frame, text="Пропускать файлы более", 
                      variable=self.app.skip_large_files).pack(side=tk.LEFT)
        
        # Добавляем новую опцию для указания размера
        if not hasattr(self.app, 'max_file_size'):
            self.app.max_file_size = tk.IntVar(value=100)
            
        size_spinbox = ttk.Spinbox(size_frame, from_=1, to=1000, width=5, 
                                textvariable=self.app.max_file_size)
        size_spinbox.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(size_frame, text="МБ").pack(side=tk.LEFT)
        
        # Настройки глубины обхода
        depth_frame = ttk.Frame(left_column)
        depth_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(depth_frame, text="Макс. глубина обхода папок:").pack(side=tk.LEFT)
        
        # Добавляем новую опцию для указания глубины
        if not hasattr(self.app, 'max_depth'):
            self.app.max_depth = tk.IntVar(value=10)
            
        depth_spinbox = ttk.Spinbox(depth_frame, from_=1, to=100, width=5, 
                                  textvariable=self.app.max_depth)
        depth_spinbox.pack(side=tk.LEFT, padx=2)
        
        # Правая колонка
        right_column = ttk.Frame(advanced_frame)
        right_column.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(20, 0))
        
        # Настройки потоков
        threads_frame = ttk.Frame(right_column)
        threads_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(threads_frame, text="Макс. количество потоков: ").pack(side=tk.LEFT)
        
        threads_spinbox = ttk.Spinbox(threads_frame, from_=1, to=32, width=5, 
                                    textvariable=self.app.max_threads)
        threads_spinbox.pack(side=tk.LEFT, padx=2)
        
        # Дополнительные опции
        recursion_frame = ttk.Frame(right_column)
        recursion_frame.pack(fill=tk.X, pady=2)
        
        # Добавляем новую опцию для рекурсивного обхода
        if not hasattr(self.app, 'recursive_search'):
            self.app.recursive_search = tk.BooleanVar(value=True)
            
        ttk.Checkbutton(recursion_frame, text="Рекурсивный обход папок", 
                      variable=self.app.recursive_search).pack(anchor=tk.W)
        
        # Добавляем опцию для показа скрытых файлов
        if not hasattr(self.app, 'show_hidden'):
            self.app.show_hidden = tk.BooleanVar(value=False)
            
        ttk.Checkbutton(right_column, text="Включать скрытые файлы в проверку", 
                      variable=self.app.show_hidden).pack(anchor=tk.W, pady=2)

    def create_search_values_panel(self, parent_frame):
        """
        Создает улучшенную панель для поиска значений
        """
        search_frame = ttk.LabelFrame(parent_frame, text="Поиск значений в документах", padding="10")
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Добавляем флажок для включения поиска
        enable_frame = ttk.Frame(search_frame)
        enable_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Checkbutton(enable_frame, text="Дополнительный поиск значений", 
                      variable=self.app.enable_value_search).pack(side=tk.LEFT)
        
        # Добавляем новую опцию для регистрозависимого поиска
        if not hasattr(self.app, 'case_sensitive'):
            self.app.case_sensitive = tk.BooleanVar(value=False)
            
        ttk.Checkbutton(enable_frame, text="С учетом регистра", 
                      variable=self.app.case_sensitive).pack(side=tk.LEFT, padx=20)
        
        # Поле для ввода значений с меткой
        values_label_frame = ttk.Frame(search_frame)
        values_label_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(values_label_frame, text="Значения для поиска:").pack(anchor=tk.W)
        
        # Многострочное поле ввода для большего удобства
        values_frame = ttk.Frame(search_frame)
        values_frame.pack(fill=tk.X, pady=2)
        
        # Создаем текстовое поле вместо entry для удобства ввода нескольких значений
        if not hasattr(self.app, 'search_values_text'):
            self.app.search_values_text = tk.Text(values_frame, height=4, width=50)
            if hasattr(self.app, 'search_values'):
                self.app.search_values_text.insert('1.0', self.app.search_values.get())
                
        self.app.search_values_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Добавляем прокрутку
        scrollbar = ttk.Scrollbar(values_frame, orient=tk.VERTICAL, command=self.app.search_values_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.app.search_values_text.config(yscrollcommand=scrollbar.set)
        
        # Подсказка и пример
        hint_text = ("Укажите значения для поиска в формате: \"2024\", \"Привет_\", \"Предоставлено \", ...\n"
                     "Значения должны быть заключены в двойные кавычки и разделены запятыми. "
                     "Пробелы и другие символы учитываются.")
        ttk.Label(search_frame, text=hint_text, 
                 font=("", 8, "italic"), foreground="#666666").pack(anchor=tk.W, pady=2)
        
        # Кнопки для управления списком значений
        buttons_frame = ttk.Frame(search_frame)
        buttons_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(buttons_frame, text="Добавить из файла", 
                 command=self.load_search_values, width=15).pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="Очистить", 
                 command=self.clear_search_values, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="Проверить формат", 
                 command=self.validate_search_values, width=15).pack(side=tk.LEFT, padx=2)

    def create_output_panel(self, parent_frame):
        """
        Создает улучшенную панель для настройки вывода и отчетов
        """
        output_frame = ttk.LabelFrame(parent_frame, text="Настройки отчета", padding="10")
        output_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Путь сохранения
        path_frame = ttk.Frame(output_frame)
        path_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(path_frame, text="Путь сохранения отчета:").pack(side=tk.LEFT, padx=(0, 10))
        
        output_entry = ttk.Entry(path_frame, textvariable=self.app.output_path, width=50)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        output_button = ttk.Button(path_frame, text="Выбрать", 
                                 command=self.app.browse_output_path, width=10)
        output_button.pack(side=tk.LEFT)
        
        # Формат отчета
        format_frame = ttk.Frame(output_frame)
        format_frame.pack(fill=tk.X, pady=(10, 2))
        
        ttk.Label(format_frame, text="Формат отчета:").pack(side=tk.LEFT, padx=(0, 10))
        
        # Добавляем новую опцию для формата отчета
        if not hasattr(self.app, 'report_format'):
            self.app.report_format = tk.StringVar(value="xlsx")
            
        ttk.Radiobutton(format_frame, text="Excel (XLSX)", 
                      variable=self.app.report_format, value="xlsx").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(format_frame, text="CSV", 
                      variable=self.app.report_format, value="csv").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(format_frame, text="HTML", 
                      variable=self.app.report_format, value="html").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(format_frame, text="JSON", 
                      variable=self.app.report_format, value="json").pack(side=tk.LEFT, padx=5)
        
        # Дополнительные опции отчета
        options_frame = ttk.Frame(output_frame)
        options_frame.pack(fill=tk.X, pady=5)
        
        # Добавляем новые опции для настройки отчета
        if not hasattr(self.app, 'auto_open_report'):
            self.app.auto_open_report = tk.BooleanVar(value=True)
            
        if not hasattr(self.app, 'include_timestamp'):
            self.app.include_timestamp = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(options_frame, text="Автоматически открывать отчет", 
                      variable=self.app.auto_open_report).pack(side=tk.LEFT, padx=(0, 20))
                      
        ttk.Checkbutton(options_frame, text="Добавлять временную метку к имени файла", 
                      variable=self.app.include_timestamp).pack(side=tk.LEFT)

    def create_presets_panel(self, parent_frame):
        """
        Создает новую панель для сохранения и загрузки предустановок настроек
        """
        presets_frame = ttk.LabelFrame(parent_frame, text="Предустановки настроек", padding="10")
        presets_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Верхняя часть с описанием
        ttk.Label(presets_frame, 
                text="Сохраняйте и загружайте предустановки настроек для разных типов проверок").pack(anchor=tk.W, pady=(0, 5))
        
        # Фрейм для выбора предустановки
        select_frame = ttk.Frame(presets_frame)
        select_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(select_frame, text="Выбрать предустановку:").pack(side=tk.LEFT, padx=(0, 10))
        
        # Добавляем новую опцию для хранения предустановок
        if not hasattr(self.app, 'current_preset'):
            self.app.current_preset = tk.StringVar(value="Стандартная")
            
        # Комбобокс для выбора пресета
        presets_combo = ttk.Combobox(select_frame, textvariable=self.app.current_preset, 
                                  values=["Стандартная", "Быстрая проверка", "Полная проверка"])
        presets_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Привязываем событие выбора
        presets_combo.bind("<<ComboboxSelected>>", self.load_preset)
        
        load_button = ttk.Button(select_frame, text="Загрузить", 
                              command=self.load_selected_preset, width=10)
        load_button.pack(side=tk.LEFT, padx=2)
        
        # Фрейм для сохранения предустановки
        save_frame = ttk.Frame(presets_frame)
        save_frame.pack(fill=tk.X, pady=(10, 2))
        
        ttk.Label(save_frame, text="Имя новой предустановки:").pack(side=tk.LEFT, padx=(0, 10))
        
        # Добавляем новую опцию для имени новой предустановки
        if not hasattr(self.app, 'new_preset_name'):
            self.app.new_preset_name = tk.StringVar()
            
        preset_entry = ttk.Entry(save_frame, textvariable=self.app.new_preset_name, width=30)
        preset_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        save_button = ttk.Button(save_frame, text="Сохранить текущие", 
                               command=self.save_current_preset, width=15)
        save_button.pack(side=tk.LEFT)

    # Вспомогательные методы для новой функциональности

    def select_all_file_types(self):
        """Выбирает все типы файлов"""
        for var in [self.app.check_docx, self.app.check_doc, self.app.check_docm,
                   self.app.check_xlsx, self.app.check_xls, self.app.check_xlsm]:
            var.set(True)

    def deselect_all_file_types(self):
        """Снимает выбор со всех типов файлов"""
        for var in [self.app.check_docx, self.app.check_doc, self.app.check_docm,
                   self.app.check_xlsx, self.app.check_xls, self.app.check_xlsm]:
            var.set(False)

    def select_only_word(self):
        """Выбирает только форматы Word"""
        self.deselect_all_file_types()
        for var in [self.app.check_docx, self.app.check_doc, self.app.check_docm]:
            var.set(True)

    def select_only_excel(self):
        """Выбирает только форматы Excel"""
        self.deselect_all_file_types()
        for var in [self.app.check_xlsx, self.app.check_xls, self.app.check_xlsm]:
            var.set(True)

    def load_search_values(self):
        """Загружает значения для поиска из текстового файла"""
        # Реализация будет добавлена в основном приложении
        if hasattr(self.app, 'load_search_values_from_file'):
            self.app.load_search_values_from_file()
        else:
            print("Метод load_search_values_from_file не реализован")

    def clear_search_values(self):
        """Очищает поле со значениями для поиска"""
        if hasattr(self.app, 'search_values_text'):
            self.app.search_values_text.delete('1.0', tk.END)

    def validate_search_values(self):
        """Проверяет формат введенных значений для поиска"""
        # Реализация будет добавлена в основном приложении
        if hasattr(self.app, 'validate_search_values_format'):
            self.app.validate_search_values_format()
        else:
            print("Метод validate_search_values_format не реализован")

    def load_preset(self, event):
        """Обрабатывает выбор предустановки в выпадающем списке"""
        self.load_selected_preset()

    def load_selected_preset(self):
        """Загружает выбранную предустановку настроек"""
        # Реализация будет добавлена в основном приложении
        if hasattr(self.app, 'load_settings_preset'):
            self.app.load_settings_preset(self.app.current_preset.get())
        else:
            print(f"Загрузка предустановки: {self.app.current_preset.get()}")

    def save_current_preset(self):
        """Сохраняет текущие настройки как предустановку"""
        # Реализация будет добавлена в основном приложении
        preset_name = self.app.new_preset_name.get()
        if not preset_name:
            # Показываем предупреждение, если имя не указано
            import tkinter.messagebox as messagebox
            messagebox.showwarning("Предупреждение", "Укажите имя для сохранения предустановки")
            return
            
        if hasattr(self.app, 'save_settings_preset'):
            self.app.save_settings_preset(preset_name)
        else:
            print(f"Сохранение предустановки: {preset_name}")
            # Обновляем список доступных предустановок
            all_presets = list(self.app.current_preset['values'])
            if preset_name not in all_presets:
                all_presets.append(preset_name)
                self.app.current_preset.config(values=all_presets)
            self.app.current_preset.set(preset_name)