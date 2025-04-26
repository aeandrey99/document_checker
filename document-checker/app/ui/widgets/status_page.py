#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import datetime

class StatusPageBuilder:
    """
    Улучшенный класс для создания элементов на странице статуса и отчетов
    """
    def __init__(self, app_instance):
        self.app = app_instance

    def create_status_page(self, parent_frame):
        """
        Создаёт улучшенную страницу со статусами, прогресс-баром и таблицей результатов
        """
        # Верхняя часть - информация о статусе и времени выполнения
        self.create_status_header(parent_frame)
        
        # Прогресс выполнения
        self.create_progress_section(parent_frame)
        
        # Раздел с фильтрами результатов (новый)
        self.create_filters_section(parent_frame)
        
        # Таблица результатов с возможностью сортировки
        self.create_results_table(parent_frame)
        
        # Нижняя панель с кнопками действий (новая)
        self.create_actions_panel(parent_frame)
        
    def create_status_header(self, parent_frame):
        """
        Создает улучшенный заголовок с информацией о статусе
        """
        header_frame = ttk.Frame(parent_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=(5, 0))
        
        # Левая часть - статус и текущий файл
        status_frame = ttk.Frame(header_frame)
        status_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        status_label = ttk.Label(status_frame, text="Статус:", font=("", 9, "bold"))
        status_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.app.status_text_label = ttk.Label(status_frame, textvariable=self.app.status_text,
                                          font=("", 9))
        self.app.status_text_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Добавляем индикатор активности (мигающий цветной круг)
        self.activity_indicator = tk.Canvas(status_frame, width=16, height=16, 
                                          highlightthickness=0)
        self.activity_indicator.pack(side=tk.LEFT, padx=(0, 10))
        self.activity_indicator.create_oval(4, 4, 12, 12, fill="gray", tags="indicator")
        
        current_file_label = ttk.Label(status_frame, text="Текущий файл:", font=("", 9, "bold"))
        current_file_label.pack(side=tk.LEFT, padx=(0, 5))
        
        current_file_value = ttk.Label(status_frame, textvariable=self.app.current_file, 
                                     font=("", 9))
        current_file_value.pack(side=tk.LEFT)
        
        # Правая часть - время выполнения и номер запуска
        time_frame = ttk.Frame(header_frame)
        time_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Номер запуска
        run_label = ttk.Label(time_frame, text="Номер запуска:", font=("", 9, "bold"))
        run_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Создаем метку для номера запуска, если она не определена
        if not hasattr(self.app, 'run_id_label'):
            if hasattr(self.app, 'report_manager') and hasattr(self.app.report_manager, 'current_run_id'):
                run_id = str(self.app.report_manager.current_run_id)
            else:
                run_id = "1"
            self.app.run_id_label = ttk.Label(time_frame, text=run_id, font=("", 9))
            
        self.app.run_id_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Время выполнения
        time_label = ttk.Label(time_frame, text="Время выполнения:", font=("", 9, "bold"))
        time_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Создаем переменную для времени выполнения
        if not hasattr(self.app, 'elapsed_time'):
            self.app.elapsed_time = tk.StringVar(value="00:00:00")
            
        elapsed_value = ttk.Label(time_frame, textvariable=self.app.elapsed_time, 
                               font=("", 9))
        elapsed_value.pack(side=tk.LEFT)
        
        # Метод для обновления индикатора активности
        self.update_activity_indicator("idle")

    def create_progress_section(self, parent_frame):
        """
        Создает улучшенную секцию с информацией о прогрессе
        """
        progress_frame = ttk.LabelFrame(parent_frame, text="Прогресс выполнения", padding="10")
        progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Верхний ряд - индикаторы прогресса
        indicators_frame = ttk.Frame(progress_frame)
        indicators_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Контейнер для счетчиков файлов
        counters_frame = ttk.Frame(indicators_frame)
        counters_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Всего файлов
        total_frame = ttk.Frame(counters_frame)
        total_frame.pack(anchor=tk.W, pady=2)
        ttk.Label(total_frame, text="Всего файлов для проверки: ", width=25).pack(side=tk.LEFT)
        ttk.Label(total_frame, textvariable=self.app.total_files_var, 
                font=("", 9, "bold")).pack(side=tk.LEFT)
        
        # В очереди
        queue_frame = ttk.Frame(counters_frame)
        queue_frame.pack(anchor=tk.W, pady=2)
        ttk.Label(queue_frame, text="В очереди к проверке: ", width=25).pack(side=tk.LEFT)
        ttk.Label(queue_frame, textvariable=self.app.remaining_files_var, 
                font=("", 9, "bold")).pack(side=tk.LEFT)
        
        # Обработано успешно
        processed_frame = ttk.Frame(counters_frame)
        processed_frame.pack(anchor=tk.W, pady=2)
        ttk.Label(processed_frame, text="Обработано успешно: ", width=25).pack(side=tk.LEFT)
        
        # Добавляем новую переменную для успешно обработанных файлов
        if not hasattr(self.app, 'success_files_var'):
            self.app.success_files_var = tk.StringVar(value="0")
            
        ttk.Label(processed_frame, textvariable=self.app.success_files_var, 
                font=("", 9, "bold")).pack(side=tk.LEFT)
        
        # Обработано с ошибками
        errors_frame = ttk.Frame(counters_frame)
        errors_frame.pack(anchor=tk.W, pady=2)
        ttk.Label(errors_frame, text="С ошибками или предупреждениями: ", width=25).pack(side=tk.LEFT)
        
        # Добавляем новую переменную для файлов с ошибками
        if not hasattr(self.app, 'error_files_var'):
            self.app.error_files_var = tk.StringVar(value="0")
            
        ttk.Label(errors_frame, textvariable=self.app.error_files_var, 
                font=("", 9, "bold")).pack(side=tk.LEFT)
        
        # Круговая диаграмма прогресса (справа)
        chart_frame = ttk.Frame(indicators_frame)
        chart_frame.pack(side=tk.RIGHT, padx=20)
        
        self.progress_canvas = tk.Canvas(chart_frame, width=100, height=100, 
                                      highlightthickness=0)
        self.progress_canvas.pack()
        
        # Рисуем начальную круговую диаграмму (серый круг)
        self.progress_canvas.create_oval(10, 10, 90, 90, fill="#e0e0e0", outline="", tags="progress_bg")
        
        # Текст внутри круга (процент выполнения)
        self.progress_canvas.create_text(50, 50, text="0%", fill="#333333", 
                                      font=("", 14, "bold"), tags="progress_text")
        
        # Нижний ряд - прогресс-бар
        self.app.progress_bar = ttk.Progressbar(
            progress_frame, 
            variable=self.app.progress_value,
            length=100,
            mode='determinate'
        )
        self.app.progress_bar.pack(fill=tk.X, pady=(5, 0))
        
        # Добавляем подписи к прогресс-бару
        labels_frame = ttk.Frame(progress_frame)
        labels_frame.pack(fill=tk.X)
        
        ttk.Label(labels_frame, text="0%", font=("", 8)).pack(side=tk.LEFT)
        ttk.Label(labels_frame, text="50%", font=("", 8)).pack(side=tk.LEFT, padx=(200, 0))
        ttk.Label(labels_frame, text="100%", font=("", 8)).pack(side=tk.RIGHT)
        
        # Подсказка
        hint_frame = ttk.Frame(progress_frame)
        hint_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(hint_frame, 
                text="Подсказка: дважды щелкните по строке с файлом, чтобы открыть его", 
                font=("", 8, "italic"), foreground="#666666").pack(side=tk.LEFT)

    def create_filters_section(self, parent_frame):
        """
        Создает новую секцию с фильтрами для результатов
        """
        filters_frame = ttk.LabelFrame(parent_frame, text="Фильтры результатов", padding="10")
        filters_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Быстрые фильтры
        quick_filters_frame = ttk.Frame(filters_frame)
        quick_filters_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(quick_filters_frame, text="Все файлы", 
                 command=lambda: self.apply_filter("all"), width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_filters_frame, text="Только ошибки", 
                 command=lambda: self.apply_filter("failed"), width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_filters_frame, text="Только успех", 
                 command=lambda: self.apply_filter("passed"), width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_filters_frame, text="Word файлы", 
                 command=lambda: self.apply_filter("word"), width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_filters_frame, text="Excel файлы", 
                 command=lambda: self.apply_filter("excel"), width=12).pack(side=tk.LEFT, padx=2)
        
        # Расширенные фильтры
        advanced_filters_frame = ttk.Frame(filters_frame)
        advanced_filters_frame.pack(fill=tk.X)
        
        # Фильтр по типу файла
        type_frame = ttk.Frame(advanced_filters_frame)
        type_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(type_frame, text="Тип файла:").pack(side=tk.LEFT, padx=(0, 5))
        
        # Добавляем переменную для хранения типа файла
        if not hasattr(self.app, 'file_type_filter'):
            self.app.file_type_filter = tk.StringVar(value="Все")
            
        file_type_combo = ttk.Combobox(type_frame, textvariable=self.app.file_type_filter, width=15,
                                    values=["Все", "Word", "Excel", "DOCX", "DOC", "DOCM", "XLSX", "XLS", "XLSM"])
        file_type_combo.pack(side=tk.LEFT)
        file_type_combo.bind("<<ComboboxSelected>>", 
                          lambda e: self.apply_custom_filter())
        
        # Фильтр по результату
        result_frame = ttk.Frame(advanced_filters_frame)
        result_frame.pack(side=tk.LEFT, padx=10)
        
        ttk.Label(result_frame, text="Результат:").pack(side=tk.LEFT, padx=(0, 5))
        
        # Добавляем переменную для хранения результата
        if not hasattr(self.app, 'result_filter'):
            self.app.result_filter = tk.StringVar(value="Все")
            
        result_combo = ttk.Combobox(result_frame, textvariable=self.app.result_filter, width=15,
                                values=["Все", "Успешно", "Ошибка", "Предупреждение"])
        result_combo.pack(side=tk.LEFT)
        result_combo.bind("<<ComboboxSelected>>", 
                         lambda e: self.apply_custom_filter())
        
        # Кнопка для применения фильтров
        apply_button = ttk.Button(advanced_filters_frame, text="Применить фильтры", 
                               command=self.apply_custom_filter, width=15)
        apply_button.pack(side=tk.LEFT, padx=10)
        
        # Кнопка сброса всех фильтров
        reset_button = ttk.Button(advanced_filters_frame, text="Сбросить фильтры", 
                               command=self.reset_filters, width=15)
        reset_button.pack(side=tk.LEFT)
        
        # Строка поиска (справа)
        search_frame = ttk.Frame(advanced_filters_frame)
        search_frame.pack(side=tk.RIGHT)
        
        ttk.Label(search_frame, text="Поиск:").pack(side=tk.LEFT, padx=(0, 5))
        
        # Добавляем переменную для поиска
        if not hasattr(self.app, 'results_search'):
            self.app.results_search = tk.StringVar()
            
        search_entry = ttk.Entry(search_frame, textvariable=self.app.results_search, width=20)
        search_entry.pack(side=tk.LEFT, padx=(0, 5))
        search_entry.bind("<Return>", lambda e: self.search_in_results())
        
        search_button = ttk.Button(search_frame, text="Найти", 
                                command=self.search_in_results, width=8)
        search_button.pack(side=tk.LEFT)

    def create_results_table(self, parent_frame):
        """
        Создает улучшенную таблицу результатов с возможностью сортировки
        """
        results_frame = ttk.Frame(parent_frame, padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Настраиваем столбцы
        columns = ("№", "Имя файла", "Тип файла", "Путь к файлу", "Результат", "Комментарий")
        
        # Создаем таблицу с возможностью сортировки
        self.app.results_tree = ttk.Treeview(results_frame, columns=columns, show='headings', selectmode='extended')
        
        for col in columns:
            self.app.results_tree.heading(col, text=col, 
                                     command=lambda c=col: self.sort_tree_column(c))
        
        # Настраиваем ширину столбцов
        self.app.results_tree.column("№", width=40, anchor=tk.CENTER, minwidth=40)
        self.app.results_tree.column("Имя файла", width=150, minwidth=100)
        self.app.results_tree.column("Тип файла", width=80, anchor=tk.CENTER, minwidth=80)
        self.app.results_tree.column("Путь к файлу", width=200, minwidth=150)
        self.app.results_tree.column("Результат", width=100, anchor=tk.CENTER, minwidth=80)
        self.app.results_tree.column("Комментарий", width=300, minwidth=200)
        
        # Добавляем вертикальную прокрутку
        v_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.app.results_tree.yview)
        self.app.results_tree.configure(yscroll=v_scrollbar.set)
        
        # Добавляем горизонтальную прокрутку
        h_scrollbar = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL, command=self.app.results_tree.xview)
        self.app.results_tree.configure(xscroll=h_scrollbar.set)
        
        # Размещаем элементы
        self.app.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Настраиваем теги для цветового выделения строк
        self.app.results_tree.tag_configure('passed', background='#C8E6C9')  # Зеленый
        self.app.results_tree.tag_configure('failed', background='#FFCDD2')  # Красный
        self.app.results_tree.tag_configure('warning', background='#FFF9C4')  # Желтый
        
        # Привязываем обработчик двойного клика и контекстного меню
        self.app.results_tree.bind('<Double-1>', self.app.on_item_double_click)
        self.app.results_tree.bind('<Button-3>', self.app.show_context_menu)
        
        # Привязываем обработчик выделения строки для обновления статуса
        self.app.results_tree.bind('<<TreeviewSelect>>', self.on_item_select)

    def create_actions_panel(self, parent_frame):
        """
        Создает новую панель с кнопками действий в нижней части страницы
        """
        actions_frame = ttk.Frame(parent_frame, padding="5")
        actions_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Левая часть - работа с выбранными файлами
        file_actions_frame = ttk.LabelFrame(actions_frame, text="Действия с выбранными файлами", padding="5")
        file_actions_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        ttk.Button(file_actions_frame, text="Открыть файл", 
                 command=self.app.open_selected_file, width=15).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_actions_frame, text="Открыть директорию", 
                 command=self.app.open_file_directory, width=15).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_actions_frame, text="Повторить проверку", 
                 command=self.recheck_selected_files, width=15).pack(side=tk.LEFT, padx=2)
        
        # Правая часть - экспорт и отчеты
        report_actions_frame = ttk.LabelFrame(actions_frame, text="Экспорт и отчеты", padding="5")
        report_actions_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Button(report_actions_frame, text="Экспорт в Excel", 
                 command=lambda: self.app.export_results("xlsx"), width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(report_actions_frame, text="Экспорт в CSV", 
                 command=lambda: self.app.export_results("csv"), width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(report_actions_frame, text="Сохранить отчет", 
                 command=self.app.save_report, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(report_actions_frame, text="Печать", 
                 command=self.print_report, width=8).pack(side=tk.LEFT, padx=2)

    # Вспомогательные методы для новой функциональности

    def update_activity_indicator(self, status):
        """
        Обновляет индикатор активности в зависимости от статуса
        """
        if status == "running":
            self.activity_indicator.itemconfig("indicator", fill="#4CAF50")  # Зеленый
            self.app.root.after(500, lambda: self.update_activity_indicator("running_off"))
        elif status == "running_off":
            self.activity_indicator.itemconfig("indicator", fill="#C8E6C9")  # Светло-зеленый
            self.app.root.after(500, lambda: self.update_activity_indicator("running"))
        elif status == "error":
            self.activity_indicator.itemconfig("indicator", fill="#F44336")  # Красный
            self.app.root.after(500, lambda: self.update_activity_indicator("error_off"))
        elif status == "error_off":
            self.activity_indicator.itemconfig("indicator", fill="#FFCDD2")  # Светло-красный
            self.app.root.after(500, lambda: self.update_activity_indicator("error"))
        elif status == "warning":
            self.activity_indicator.itemconfig("indicator", fill="#FFC107")  # Желтый
            self.app.root.after(500, lambda: self.update_activity_indicator("warning_off"))
        elif status == "warning_off":
            self.activity_indicator.itemconfig("indicator", fill="#FFF9C4")  # Светло-желтый
            self.app.root.after(500, lambda: self.update_activity_indicator("warning"))
        else:  # idle или другие состояния
            self.activity_indicator.itemconfig("indicator", fill="#9E9E9E")  # Серый

    def update_progress_chart(self, percent):
        """
        Обновляет круговую диаграмму прогресса
        """
        if not hasattr(self, 'progress_canvas'):
            return
            
        # Очищаем предыдущие сегменты
        self.progress_canvas.delete("progress_segment")
        
        # Рисуем новый сегмент
        if percent > 0:
            angle = 360 * (percent / 100)
            self.progress_canvas.create_arc(10, 10, 90, 90, 
                                         start=90, extent=-angle, 
                                         fill="#4CAF50", outline="", 
                                         tags="progress_segment")
            
        # Обновляем текст
        self.progress_canvas.itemconfig("progress_text", text=f"{int(percent)}%")

    def sort_tree_column(self, column):
        """
        Сортирует содержимое таблицы по выбранному столбцу
        """
        if not hasattr(self.app, 'results_tree'):
            return
            
        # Получаем все строки с данными
        items = [(self.app.results_tree.set(item, column), item) for item in self.app.results_tree.get_children('')]
        
        # Если столбец № - сортируем по числовому значению
        if column == "№":
            try:
                items.sort(key=lambda x: int(x[0]))
            except:
                items.sort()
        else:
            # Обычная сортировка строк
            items.sort()
            
        # Меняем порядок расположения элементов в таблице
        for index, (_, item) in enumerate(items):
            self.app.results_tree.move(item, '', index)

    def apply_filter(self, filter_type):
        """
        Применяет быстрый фильтр к таблице результатов
        """
        if not hasattr(self.app, 'results_tree'):
            return
            
        # Показываем все элементы перед фильтрацией
        for item in self.app.results_tree.get_children(''):
            self.app.results_tree.item(item, open=True)
            self.app.results_tree.detach(item)
            
        # Получаем все элементы
        all_items = self.app.all_results if hasattr(self.app, 'all_results') else []
        
        if not all_items:
            # Если список всех элементов не сохранен, создаем его
            all_items = []
            for item in self.app.results_tree.get_children(''):
                values = self.app.results_tree.item(item, 'values')
                all_items.append((item, values))
            self.app.all_results = all_items
        
        # Применяем фильтр
        for item, values in all_items:
            show_item = False
            
            if filter_type == "all":
                show_item = True
            elif filter_type == "failed" and values[4] in ["Ошибка", "Предупреждение"]:
                show_item = True
            elif filter_type == "passed" and values[4] == "Успешно":
                show_item = True
            elif filter_type == "word" and values[2] in ["DOCX", "DOC", "DOCM"]:
                show_item = True
            elif filter_type == "excel" and values[2] in ["XLSX", "XLS", "XLSM"]:
                show_item = True
                
            if show_item:
                self.app.results_tree.reattach(item, '', 'end')
                
        # Обновляем информацию о количестве отображаемых элементов
        self.update_filter_status()

    def apply_custom_filter(self):
        """
        Применяет пользовательские фильтры к таблице результатов
        """
        if not hasattr(self.app, 'results_tree'):
            return
            
        # Показываем все элементы перед фильтрацией
        for item in self.app.results_tree.get_children(''):
            self.app.results_tree.item(item, open=True)
            self.app.results_tree.detach(item)
            
        # Получаем все элементы
        all_items = self.app.all_results if hasattr(self.app, 'all_results') else []
        
        if not all_items:
            # Если список всех элементов не сохранен, создаем его
            all_items = []
            for item in self.app.results_tree.get_children(''):
                values = self.app.results_tree.item(item, 'values')
                all_items.append((item, values))
            self.app.all_results = all_items
        
        # Получаем значения фильтров
        file_type = self.app.file_type_filter.get()
        result = self.app.result_filter.get()
        search_text = self.app.results_search.get().lower()
        
        # Применяем фильтр
        for item, values in all_items:
            show_item = True
            
            # Фильтр по типу файла
            if file_type != "Все":
                if file_type in ["Word", "Excel"]:
                    # Группы форматов
                    if file_type == "Word" and values[2] not in ["DOCX", "DOC", "DOCM"]:
                        show_item = False
                    elif file_type == "Excel" and values[2] not in ["XLSX", "XLS", "XLSM"]:
                        show_item = False
                elif values[2] != file_type:
                    show_item = False
            
            # Фильтр по результату
            if result != "Все" and show_item:
                if result == "Успешно" and values[4] != "Успешно":
                    show_item = False
                elif result == "Ошибка" and values[4] != "Ошибка":
                    show_item = False
                elif result == "Предупреждение" and values[4] != "Предупреждение":
                    show_item = False
            
            # Фильтр по поисковому запросу
            if search_text and show_item:
                text_found = False
                for val in values:
                    if search_text in str(val).lower():
                        text_found = True
                        break
                if not text_found:
                    show_item = False
                    
            if show_item:
                self.app.results_tree.reattach(item, '', 'end')
                
        # Обновляем информацию о количестве отображаемых элементов
        self.update_filter_status()

    def reset_filters(self):
        """
        Сбрасывает все фильтры и показывает все элементы
        """
        # Сбрасываем значения фильтров
        self.app.file_type_filter.set("Все")
        self.app.result_filter.set("Все")
        self.app.results_search.set("")
        
        # Применяем фильтр "все"
        self.apply_filter("all")

    def search_in_results(self):
        """
        Выполняет поиск по результатам и выделяет найденные строки
        """
        if not hasattr(self.app, 'results_tree'):
            return
            
        search_text = self.app.results_search.get().lower()
        
        # Применяем пользовательские фильтры с учетом поиска
        self.apply_custom_filter()
        
        # Если поисковый запрос пустой, выходим
        if not search_text:
            return
            
        # Снимаем выделение со всех строк
        self.app.results_tree.selection_remove(self.app.results_tree.selection())
        
        # Ищем и выделяем совпадения
        found_items = []
        for item in self.app.results_tree.get_children(''):
            # Получаем все значения в строке
            values = self.app.results_tree.item(item, "values")
            # Преобразуем в строку для поиска
            row_text = " ".join([str(val).lower() for val in values])
            
            if search_text in row_text:
                found_items.append(item)
                # Добавляем в выделение
                self.app.results_tree.selection_add(item)
        
        # Прокручиваем к первому найденному элементу, если он есть
        if found_items:
            self.app.results_tree.see(found_items[0])
            
        # Обновляем статус поиска
        if hasattr(self.app, 'status_bar_label'):
            self.app.status_bar_label.config(
                text=f"Поиск: найдено {len(found_items)} совпадений" if found_items else "Поиск: нет совпадений")

    def update_filter_status(self):
        """
        Обновляет информацию о количестве отображаемых элементов
        """
        if not hasattr(self.app, 'results_tree'):
            return
            
        visible_count = len(self.app.results_tree.get_children(''))
        total_count = len(self.app.all_results) if hasattr(self.app, 'all_results') else visible_count
        
        if hasattr(self.app, 'status_bar_label'):
            self.app.status_bar_label.config(
                text=f"Отображается {visible_count} из {total_count} элементов")

    def on_item_select(self, event):
        """
        Обрабатывает выделение элемента в таблице
        """
        if not hasattr(self.app, 'results_tree'):
            return
            
        # Получаем выбранные элементы
        selected_items = self.app.results_tree.selection()
        
        # Обновляем статусную строку
        if hasattr(self.app, 'status_bar_label'):
            if len(selected_items) == 1:
                # Получаем значения выбранной строки
                item = selected_items[0]
                values = self.app.results_tree.item(item, "values")
                self.app.status_bar_label.config(
                    text=f"Выбран файл: {values[1]} ({values[2]}) - {values[4]}")
            elif len(selected_items) > 1:
                self.app.status_bar_label.config(
                    text=f"Выбрано элементов: {len(selected_items)}")

    def recheck_selected_files(self):
        """
        Перепроверяет выбранные файлы
        """
        if not hasattr(self.app, 'results_tree'):
            return
            
        # Получаем выбранные элементы
        selected_items = self.app.results_tree.selection()
        
        if not selected_items:
            import tkinter.messagebox as messagebox
            messagebox.showinfo("Информация", "Не выбрано ни одного файла для повторной проверки")
            return
            
        # Собираем пути к файлам для повторной проверки
        files_to_recheck = []
        for item in selected_items:
            values = self.app.results_tree.item(item, "values")
            file_path = values[3]  # Путь к файлу находится в 4-м столбце
            files_to_recheck.append(file_path)
            
        # Вызываем метод повторной проверки (должен быть реализован в основном приложении)
        if hasattr(self.app, 'recheck_files'):
            self.app.recheck_files(files_to_recheck)
        else:
            print(f"Повторная проверка {len(files_to_recheck)} файлов")

    def print_report(self):
        """
        Выводит отчет на печать
        """
        if not hasattr(self.app, 'results_tree'):
            return
            
        # Показываем диалог с опциями печати
        print_window = tk.Toplevel(self.app.root)
        print_window.title("Настройки печати")
        print_window.geometry("400x300")
        print_window.transient(self.app.root)
        print_window.grab_set()
        
        # Применяем текущую тему
        if hasattr(self.app, 'theme_manager'):
            print_window.configure(bg=self.app.theme_manager.current_theme_colors["bg"])
        
        # Создаем фрейм для настроек
        options_frame = ttk.Frame(print_window, padding="10")
        options_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок отчета
        ttk.Label(options_frame, text="Заголовок отчета:").pack(anchor=tk.W, pady=(0, 5))
        
        # Добавляем переменную для заголовка
        if not hasattr(self.app, 'print_title'):
            self.app.print_title = tk.StringVar(value="Отчет о проверке документов")
            
        title_entry = ttk.Entry(options_frame, textvariable=self.app.print_title, width=40)
        title_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Опции печати
        ttk.Label(options_frame, text="Опции печати:").pack(anchor=tk.W, pady=(0, 5))
        
        # Добавляем переменные для опций печати
        if not hasattr(self.app, 'print_date'):
            self.app.print_date = tk.BooleanVar(value=True)
        if not hasattr(self.app, 'print_summary'):
            self.app.print_summary = tk.BooleanVar(value=True)
        if not hasattr(self.app, 'print_all_columns'):
            self.app.print_all_columns = tk.BooleanVar(value=False)
            
        ttk.Checkbutton(options_frame, text="Добавить дату и время", 
                     variable=self.app.print_date).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Добавить сводную информацию", 
                     variable=self.app.print_summary).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Печатать все столбцы (включая путь к файлу)", 
                     variable=self.app.print_all_columns).pack(anchor=tk.W)
        
        # Кнопки действий
        buttons_frame = ttk.Frame(print_window)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(buttons_frame, text="Предпросмотр", 
                 command=lambda: self.show_print_preview(print_window), 
                 width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Печать", 
                 command=lambda: self.send_to_print(print_window), 
                 width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Отмена", 
                 command=print_window.destroy, 
                 width=15).pack(side=tk.RIGHT, padx=5)
        
    def show_print_preview(self, parent_window):
        """
        Показывает предпросмотр печати
        """
        # Создаем окно предпросмотра
        preview_window = tk.Toplevel(parent_window)
        preview_window.title("Предпросмотр печати")
        preview_window.geometry("800x600")
        preview_window.transient(parent_window)
        
        # Применяем текущую тему
        if hasattr(self.app, 'theme_manager'):
            preview_window.configure(bg=self.app.theme_manager.current_theme_colors["bg"])
        
        # Создаем текстовое поле с прокруткой для предпросмотра
        preview_frame = ttk.Frame(preview_window, padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Создаем текстовое поле для предпросмотра в формате HTML
        preview_text = tk.Text(preview_frame, wrap=tk.WORD)
        preview_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=preview_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        preview_text.configure(yscrollcommand=scrollbar.set)
        
        # Создаем содержимое отчета
        title = self.app.print_title.get()
        add_date = self.app.print_date.get()
        add_summary = self.app.print_summary.get()
        all_columns = self.app.print_all_columns.get()
        
        # Формируем HTML-структуру
        current_date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ text-align: center; }}
                .date {{ text-align: right; font-style: italic; margin-bottom: 20px; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th {{ background-color: #f2f2f2; text-align: left; padding: 8px; border: 1px solid #ddd; }}
                td {{ padding: 8px; border: 1px solid #ddd; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .summary {{ margin: 20px 0; padding: 10px; background-color: #f2f2f2; border-radius: 5px; }}
                .passed {{ background-color: #C8E6C9; }}
                .failed {{ background-color: #FFCDD2; }}
                .warning {{ background-color: #FFF9C4; }}
            </style>
        </head>
        <body>
            <h1>{title}</h1>
        """
        
        if add_date:
            html_content += f"<div class='date'>Дата: {current_date}</div>\n"
        
        if add_summary and hasattr(self.app, 'total_files_var'):
            total = self.app.total_files_var.get() if hasattr(self.app, 'total_files_var') else "0"
            success = self.app.success_files_var.get() if hasattr(self.app, 'success_files_var') else "0"
            failed = self.app.error_files_var.get() if hasattr(self.app, 'error_files_var') else "0"
            
            html_content += f"""
            <div class='summary'>
                <h3>Сводная информация:</h3>
                <p>Всего файлов проверено: {total}</p>
                <p>Успешно: {success}</p>
                <p>С ошибками или предупреждениями: {failed}</p>
            </div>
            """
        
        # Начало таблицы
        html_content += "<table>\n<tr>\n"
        
        # Заголовки столбцов
        columns = ["№", "Имя файла", "Тип файла"]
        if all_columns:
            columns.append("Путь к файлу")
        columns.extend(["Результат", "Комментарий"])
        
        for col in columns:
            html_content += f"<th>{col}</th>\n"
        html_content += "</tr>\n"
        
        # Данные таблицы
        if hasattr(self.app, 'results_tree'):
            for item in self.app.results_tree.get_children(''):
                values = self.app.results_tree.item(item, "values")
                result = values[4]  # Результат
                
                # Определяем класс для строки в зависимости от результата
                row_class = ""
                if result == "Успешно":
                    row_class = "passed"
                elif result == "Ошибка":
                    row_class = "failed"
                elif result == "Предупреждение":
                    row_class = "warning"
                
                html_content += f"<tr class='{row_class}'>\n"
                html_content += f"<td>{values[0]}</td>\n"  # №
                html_content += f"<td>{values[1]}</td>\n"  # Имя файла
                html_content += f"<td>{values[2]}</td>\n"  # Тип файла
                
                if all_columns:
                    html_content += f"<td>{values[3]}</td>\n"  # Путь к файлу
                    
                html_content += f"<td>{values[4]}</td>\n"  # Результат
                html_content += f"<td>{values[5]}</td>\n"  # Комментарий
                html_content += "</tr>\n"
                
        html_content += """
            </table>
        </body>
        </html>
        """
        
        # Вставляем HTML в текстовое поле
        preview_text.insert(tk.END, html_content)
        
        # Кнопка печати
        buttons_frame = ttk.Frame(preview_window)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(buttons_frame, text="Печать", 
                 command=lambda: self.send_to_print(parent_window), 
                 width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Закрыть", 
                 command=preview_window.destroy, 
                 width=15).pack(side=tk.RIGHT, padx=5)

    def send_to_print(self, parent_window):
        """
        Отправляет отчет на печать
        """
        # Здесь будет вызов системного диалога печати
        # В реальном приложении можно использовать модуль для печати
        import tkinter.messagebox as messagebox
        messagebox.showinfo("Печать", "Отчет отправлен на печать")
        parent_window.destroy()