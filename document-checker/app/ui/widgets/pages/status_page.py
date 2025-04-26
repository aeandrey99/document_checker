#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from ...theme import FONT_SMALL_ITALIC, TEXT_HINT, SUCCESS, ERROR
from ...widgets.common.tooltips import create_tooltip

class StatusPageBuilder:
    """
    Класс для создания элементов на странице статуса и отчетов с улучшенным интерфейсом
    """
    def __init__(self, app_instance):
        self.app = app_instance
        self.sort_order = {}  # Для хранения порядка сортировки столбцов

    def create_status_page(self, parent_frame):
        """
        Создаёт страницу со статусами, прогресс-баром и таблицей результатов
        """
        # Создаем панель статуса и текущего файла
        self.create_status_panel(parent_frame)
        
        # Создаем прогресс-бар с анимацией
        self.create_progress_bar(parent_frame)
        
        # Создаем фильтры для таблицы результатов
        self.create_filters_panel(parent_frame)
        
        # Создаем таблицу результатов
        self.create_results_table(parent_frame)
        
    def create_status_panel(self, parent_frame=None):
        """
        Создает панель статуса и текущего файла с улучшенным форматированием
        """
        if parent_frame is None:
            parent_frame = self.app.root
            
        status_frame = ttk.Frame(parent_frame, padding="10 5")
        status_frame.pack(fill=tk.X, pady=0)
        
        # Левая часть - статус проверки
        status_left_frame = ttk.Frame(status_frame)
        status_left_frame.pack(side=tk.LEFT)
        
        ttk.Label(status_left_frame, text="Статус:", font=("", 10, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        
        # Отображаем статус с цветовым индикатором
        self.status_indicator = ttk.Label(status_left_frame, textvariable=self.app.status_text)
        self.status_indicator.pack(side=tk.LEFT, padx=(0, 20))
        
        # Правая часть - информация о текущем файле
        file_frame = ttk.Frame(status_frame)
        file_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(file_frame, text="Текущий файл:", font=("", 10, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        
        # Текущий обрабатываемый файл (с обрезкой длинных путей)
        self.current_file_label = ttk.Label(file_frame, textvariable=self.app.current_file, wraplength=500)
        self.current_file_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Добавляем разделитель под статусной панелью
        separator = ttk.Separator(parent_frame, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, padx=10, pady=5)

    def create_progress_bar(self, parent_frame=None):
        """
        Создает прогресс-бар и панель с информацией о файлах
        """
        if parent_frame is None:
            parent_frame = self.app.root
            
        # Создаем рамку для прогресс-бара
        progress_frame = ttk.Frame(parent_frame, padding="10 5")
        progress_frame.pack(fill=tk.X)
        
        # Создаем рамку для счетчиков файлов
        counts_frame = ttk.Frame(progress_frame)
        counts_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Общее количество файлов
        total_frame = ttk.Frame(counts_frame)
        total_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(total_frame, text="Всего файлов:").pack(side=tk.LEFT)
        ttk.Label(total_frame, textvariable=self.app.total_files_var, 
                  font=("", 10, "bold")).pack(side=tk.LEFT, padx=(5, 0))
        
        # Осталось файлов
        remaining_frame = ttk.Frame(counts_frame)
        remaining_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(remaining_frame, text="Осталось:").pack(side=tk.LEFT)
        ttk.Label(remaining_frame, textvariable=self.app.remaining_files_var, 
                  font=("", 10, "bold")).pack(side=tk.LEFT, padx=(5, 0))
        
        # Процент выполнения
        percent_frame = ttk.Frame(counts_frame)
        percent_frame.pack(side=tk.LEFT)
        
        self.percent_var = tk.StringVar(value="0%")
        ttk.Label(percent_frame, text="Выполнено:").pack(side=tk.LEFT)
        ttk.Label(percent_frame, textvariable=self.percent_var, 
                  font=("", 10, "bold")).pack(side=tk.LEFT, padx=(5, 0))
        
        # Добавляем сам прогресс-бар
        self.app.progress_bar = ttk.Progressbar(
            progress_frame, 
            variable=self.app.progress_value,
            length=100,
            mode='determinate'
        )
        self.app.progress_bar.pack(fill=tk.X)
        
        # Привязываем обновление процента выполнения
        self.app.progress_value.trace_add("write", self._update_progress_percent)
        
        # Подсказка для пользователя
        hint_frame = ttk.Frame(parent_frame, padding="10 5")
        hint_frame.pack(fill=tk.X)
        
        ttk.Label(
            hint_frame, 
            text="Подсказка: дважды щелкните по строке с файлом, чтобы открыть его", 
            font=FONT_SMALL_ITALIC, 
            foreground=TEXT_HINT
        ).pack(side=tk.RIGHT)
    
    def _update_progress_percent(self, *args):
        """
        Обновляет отображение процента выполнения на основе значения прогресс-бара
        """
        progress = self.app.progress_value.get()
        self.percent_var.set(f"{int(progress)}%")

    def create_filters_panel(self, parent_frame=None):
        """
        Создает панель с фильтрами для таблицы результатов
        """
        if parent_frame is None:
            parent_frame = self.app.root
            
        filters_frame = ttk.Frame(parent_frame, padding="10 5")
        filters_frame.pack(fill=tk.X)
        
        # Добавляем метку Фильтры:
        ttk.Label(filters_frame, text="Фильтры:").pack(side=tk.LEFT, padx=(0, 5))
        
        # Переменная для хранения выбранного фильтра
        self.filter_var = tk.StringVar(value="all")
        
        # Создаем радиокнопки для фильтрации
        ttk.Radiobutton(
            filters_frame, 
            text="Все файлы", 
            variable=self.filter_var, 
            value="all",
            command=self._apply_filter
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            filters_frame, 
            text="Только с ошибками", 
            variable=self.filter_var, 
            value="failed",
            command=self._apply_filter
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            filters_frame, 
            text="Только успешные", 
            variable=self.filter_var, 
            value="passed",
            command=self._apply_filter
        ).pack(side=tk.LEFT, padx=5)
        
        # Поле для поиска по имени файла
        ttk.Label(filters_frame, text="Поиск:").pack(side=tk.LEFT, padx=(20, 5))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(filters_frame, textvariable=self.search_var, width=25)
        search_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        # Кнопка поиска
        search_button = ttk.Button(
            filters_frame, 
            text="Найти 🔍", 
            command=self._apply_filter
        )
        search_button.pack(side=tk.LEFT)
        
        # Привязываем событие нажатия Enter в поле поиска
        search_entry.bind("<Return>", lambda e: self._apply_filter())

    def _apply_filter(self):
        """
        Применяет фильтры и поиск к таблице результатов
        """
        # Получаем текущие значения фильтра и поиска
        filter_type = self.filter_var.get()
        search_text = self.search_var.get().lower().strip()

        # Очищаем таблицу
        for item in self.app.results_tree.get_children():
            self.app.results_tree.delete(item)

        # Фильтруем результаты
        filtered_results = []
        for result in self.app.results:
            # Фильтрация по типу результата
            if filter_type == "all":
                matches_filter = True
            elif filter_type == "passed":
                matches_filter = result['result'] == "Пройден"
            elif filter_type == "failed":
                matches_filter = result['result'] in ["Не пройден", "Ошибка", "Пропущен"]
            else:
                matches_filter = True

            # Фильтрация по строке поиска
            matches_search = True
            if search_text:
                matches_search = (
                    search_text in result['file_name'].lower() or
                    search_text in result['file_path'].lower() or
                    search_text in result['comment'].lower()
                )

            if matches_filter and matches_search:
                filtered_results.append(result)

        # Заполняем таблицу отфильтрованными результатами
        for idx, result in enumerate(filtered_results, 1):
            tag = 'passed' if result['result'] == "Пройден" else 'failed'
            self.app.results_tree.insert(
                '', 'end',
                values=(
                    idx,
                    result['file_name'],
                    result['file_type'],
                    result['file_path'],
                    result['result'],
                    result['comment']
                ),
                tags=(tag,)
            )

    def _sort_column(self, col):
        """
        Сортирует таблицу по указанному столбцу, переключая порядок сортировки
        """
        # Определяем порядок сортировки для столбца (по умолчанию восходящий)
        if col not in self.sort_order:
            self.sort_order[col] = True  # True - восходящий, False - нисходящий
        else:
            self.sort_order[col] = not self.sort_order[col]

        # Получаем текущие данные таблицы
        data = []
        for item in self.app.results_tree.get_children():
            values = self.app.results_tree.item(item, 'values')
            data.append(values)

        # Индекс столбца в данных
        col_index = {
            "№": 0,
            "Имя файла": 1,
            "Тип файла": 2,
            "Путь к файлу": 3,
            "Результат": 4,
            "Комментарий": 5
        }[col]

        # Сортируем данные
        data.sort(
            key=lambda x: x[col_index].lower() if isinstance(x[col_index], str) else x[col_index],
            reverse=not self.sort_order[col]
        )

        # Очищаем таблицу
        for item in self.app.results_tree.get_children():
            self.app.results_tree.delete(item)

        # Перезаполняем таблицу отсортированными данными
        for idx, values in enumerate(data, 1):
            tag = 'passed' if values[4] == "Пройден" else 'failed'
            self.app.results_tree.insert(
                '', 'end',
                values=(idx, *values[1:]),  # Обновляем номер строки
                tags=(tag,)
            )

    def create_results_table(self, parent_frame=None):
        """
        Создает таблицу результатов с возможностью сортировки и фильтрации
        """
        if parent_frame is None:
            parent_frame = self.app.root
            
        results_frame = ttk.Frame(parent_frame, padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Определяем колонки таблицы
        columns = ("№", "Имя файла", "Тип файла", "Путь к файлу", "Результат", "Комментарий")
        
        # Создаем таблицу
        self.app.results_tree = ttk.Treeview(
            results_frame, 
            columns=columns, 
            show='headings',
            selectmode='browse'
        )
        
        # Настраиваем заголовки и колонки
        for col in columns:
            self.app.results_tree.heading(
                col, 
                text=col,
                command=lambda c=col: self._sort_column(c)
            )
        
        # Настраиваем ширину колонок
        self.app.results_tree.column("№", width=40, anchor=tk.CENTER, stretch=False)
        self.app.results_tree.column("Имя файла", width=150, anchor=tk.W, stretch=True)
        self.app.results_tree.column("Тип файла", width=80, anchor=tk.CENTER, stretch=False)
        self.app.results_tree.column("Путь к файлу", width=200, anchor=tk.W, stretch=True)
        self.app.results_tree.column("Результат", width=100, anchor=tk.CENTER, stretch=False)
        self.app.results_tree.column("Комментарий", width=300, anchor=tk.W, stretch=True)
        
        # Добавляем вертикальную полосу прокрутки
        v_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.app.results_tree.yview)
        self.app.results_tree.configure(yscroll=v_scrollbar.set)
        
        # Добавляем горизонтальную полосу прокрутки
        h_scrollbar = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL, command=self.app.results_tree.xview)
        self.app.results_tree.configure(xscroll=h_scrollbar.set)
        
        # Размещаем элементы
        self.app.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Настраиваем теги для визуального оформления строк
        self.app.results_tree.tag_configure('passed', background='#C8E6C9')  # Светло-зеленый
        self.app.results_tree.tag_configure('failed', background='#FFCDD2')  # Светло-красный
        self.app.results_tree.tag_configure('odd', background='#F9F9F9')    # Полосатый фон для четных строк
        
        # Привязываем обработчик двойного клика
        self.app.results_tree.bind('<Double-1>', self.app.on_item_double_click)
        
        # Подсказка для пользователей
        tip_label = ttk.Label(
            parent_frame,
            text="* Нажмите на заголовок столбца для сортировки. Правый клик на строке открывает контекстное меню.",
            font=FONT_SMALL_ITALIC,
            foreground=TEXT_HINT
        )
        tip_label.pack(pady=(5, 10), anchor=tk.W, padx=10)