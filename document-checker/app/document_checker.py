#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os
import sys
import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import concurrent.futures
from queue import Queue
from tkinter import ttk

# Импортируем модули приложения
from app.ui.widgets import UIBuilder
from app.core.file_utils import normalize_path, get_file_type, is_locked_file, detect_file_size_category, open_file, open_directory
from app.core.word_checker import check_word_file
from app.core.excel_checker import check_excel_file
from app.core.report_manager import ReportManager
from app.utils.config import ConfigManager
from app.utils.threading_utils import init_workers_pool

class DocumentChecker:
    """
    Основной класс приложения для проверки документов.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Проверка документов")
        
        # Определяем переменные для отслеживания состояния
        self.selected_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.status_text = tk.StringVar(value="Готов к работе")
        self.current_file = tk.StringVar(value="Нет")
        self.progress_value = tk.IntVar(value=0)
        self.total_files_var = tk.StringVar(value="0")
        self.remaining_files_var = tk.StringVar(value="0")
        self.success_files_var = tk.StringVar(value="0")
        self.error_files_var = tk.StringVar(value="0")
        self.elapsed_time = tk.StringVar(value="00:00:00")
        
        # Переменные для настроек типов файлов
        self.check_docx = tk.BooleanVar(value=True)
        self.check_doc = tk.BooleanVar(value=True)
        self.check_docm = tk.BooleanVar(value=False)
        self.check_xlsx = tk.BooleanVar(value=True)
        self.check_xls = tk.BooleanVar(value=True)
        self.check_xlsm = tk.BooleanVar(value=False)
        
        # Дополнительные настройки
        self.skip_large_files = tk.BooleanVar(value=True)
        self.max_threads = tk.IntVar(value=4)
        self.max_file_size = tk.IntVar(value=100)
        self.max_depth = tk.IntVar(value=10)
        self.recursive_search = tk.BooleanVar(value=True)
        self.show_hidden = tk.BooleanVar(value=False)
        
        # Настройки поиска значений
        self.enable_value_search = tk.BooleanVar(value=False)
        self.search_values = tk.StringVar()
        self.case_sensitive = tk.BooleanVar(value=False)
        
        # Настройки отчетов
        self.report_format = tk.StringVar(value="xlsx")
        self.auto_open_report = tk.BooleanVar(value=True)
        self.include_timestamp = tk.BooleanVar(value=True)
        
        # Настройки предустановок
        self.current_preset = tk.StringVar(value="Стандартная")
        self.new_preset_name = tk.StringVar()
        
        # Настройки версии
        self.version = "1.0.0"
        
        # Создаем центральные компоненты приложения
        # (в вашем коде могут быть другие компоненты)
        
        # Создаем строителя интерфейса
        from app.ui.widgets import UIBuilder
        self.ui_builder = UIBuilder(self)
        
        # Создаем все элементы интерфейса
        self.ui_builder.create_widgets()
    
    def open_report_window(self):
        """
        Открывает отдельное окно с отчетом о проверенных файлах
        """
        # Если нет результатов, сообщаем об этом
        if not self.results:
            self.show_info("Отчет", "Нет данных для отображения в отчете.")
            return
        
        # Создаем новое окно
        report_window = tk.Toplevel(self.root)
        report_window.title("Отчет о проверке документов")
        report_window.geometry("900x600")
        report_window.minsize(800, 500)
        
        # Добавляем информационную панель вверху окна
        info_frame = ttk.Frame(report_window, padding="10")
        info_frame.pack(fill=tk.X)
        
        # Добавляем информацию о времени проверки
        current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        ttk.Label(info_frame, text=f"Отчет о проверке документов | Дата отчета: {current_datetime}").pack(side=tk.LEFT)
        
        # Добавляем статистику по проверке
        stats_frame = ttk.Frame(report_window, padding="10")
        stats_frame.pack(fill=tk.X)
        
        # Подсчет статистики
        total_files = len(self.results)
        passed_files = sum(1 for result in self.results if result['result'] == "Пройден")
        failed_files = sum(1 for result in self.results if result['result'] == "Не пройден")
        error_files = sum(1 for result in self.results if result['result'] in ["Ошибка", "Пропущен"])
        
        # Отображение статистики
        stats_text = f"Всего файлов: {total_files} | Пройдено: {passed_files} | Не пройдено: {failed_files} | С ошибками: {error_files}"
        ttk.Label(stats_frame, text=stats_text, font=("", 10, "bold")).pack(side=tk.LEFT)
        
        # Добавляем таблицу результатов
        tree_frame = ttk.Frame(report_window, padding="10")
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Создаем таблицу с теми же колонками, что и в основном окне
        columns = ("№", "Имя файла", "Тип файла", "Путь к файлу", "Результат", "Комментарий")
        results_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        # Настройка заголовков
        for col in columns:
            results_tree.heading(col, text=col)
        
        # Настройка ширины колонок
        results_tree.column("№", width=40, anchor=tk.CENTER)
        results_tree.column("Имя файла", width=150)
        results_tree.column("Тип файла", width=80, anchor=tk.CENTER)
        results_tree.column("Путь к файлу", width=200)
        results_tree.column("Результат", width=100, anchor=tk.CENTER)
        results_tree.column("Комментарий", width=300)
        
        # Добавление полосы прокрутки
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=results_tree.yview)
        results_tree.configure(yscroll=scrollbar.set)
        
        # Размещение таблицы и полосы прокрутки
        results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Установка тегов для цветной маркировки
        results_tree.tag_configure('passed', background='#C8E6C9')  # светло-зеленый
        results_tree.tag_configure('failed', background='#FFCDD2')  # светло-красный
        
        # Заполняем таблицу данными из результатов
        for idx, result in enumerate(self.results, 1):
            # Определение тега для строки (цвета)
            tag = 'passed' if result['result'] == "Пройден" else 'failed'
            
            # Вставка строки в таблицу
            results_tree.insert(
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
        
        # Добавляем панель с кнопками внизу
        button_frame = ttk.Frame(report_window, padding="10")
        button_frame.pack(fill=tk.X)
        
        # Кнопка для сохранения отчета в Excel
        save_button = ttk.Button(button_frame, text="Сохранить отчет в Excel", 
                            command=lambda: self.report_manager.save_results_to_excel(self.results))
        save_button.pack(side=tk.LEFT, padx=10)
        
        # Кнопка для закрытия окна
        close_button = ttk.Button(button_frame, text="Закрыть", command=report_window.destroy)
        close_button.pack(side=tk.RIGHT, padx=10)
        
        # Добавляем контекстное меню для таблицы
        self.setup_report_context_menu(report_window, results_tree)
        
        # Центрируем окно на экране
        report_window.update_idletasks()
        width = report_window.winfo_width()
        height = report_window.winfo_height()
        x = (report_window.winfo_screenwidth() // 2) - (width // 2)
        y = (report_window.winfo_screenheight() // 2) - (height // 2)
        report_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Делаем окно модальным (блокирует основное окно, пока не закроется)
        report_window.transient(self.root)
        report_window.grab_set()
        
        # Добавляем обработку изменения размера окна
        def on_report_window_resize(event):
            if event.widget == report_window:
                # Подгоняем ширину столбцов таблицы под текущий размер окна
                window_width = event.width
                
                # Подгоняем ширину последнего столбца (комментария) под оставшееся пространство
                fixed_columns_width = 40 + 150 + 80 + 200 + 100  # Сумма фиксированных ширин первых 5 столбцов
                scrollbar_width = 20  # Примерная ширина полосы прокрутки
                padding = 40  # Дополнительные отступы
                
                # Вычисляем доступную ширину для последнего столбца
                available_width = max(200, window_width - fixed_columns_width - scrollbar_width - padding)
                
                # Устанавливаем новую ширину для столбца с комментариями
                results_tree.column("Комментарий", width=available_width)
        
        # Привязываем обработчик изменения размера окна
        report_window.bind("<Configure>", on_report_window_resize)
        
        # Привязываем обработчик двойного клика для открытия файла
        results_tree.bind('<Double-1>', lambda event: self.open_file_from_tree(event, results_tree))
        
        # Отображаем окно и ждем его закрытия
        self.root.wait_window(report_window)
    
    def setup_report_context_menu(self, parent_window, tree_widget):
        """
        Настраивает контекстное меню для таблицы результатов в отдельном окне отчета
        
        Args:
            parent_window: Родительское окно (Toplevel)
            tree_widget: Виджет Treeview для отображения результатов
        """
        context_menu = tk.Menu(parent_window, tearoff=0)
        context_menu.add_command(label="Открыть файл", 
                            command=lambda: self.open_file_from_tree_selection(tree_widget))
        context_menu.add_command(label="Открыть директорию файла", 
                            command=lambda: self.open_directory_from_tree_selection(tree_widget))
        context_menu.add_separator()
        context_menu.add_command(label="Копировать путь", 
                            command=lambda: self.copy_path_from_tree_selection(tree_widget))
        
        # Привязываем контекстное меню к правому клику
        tree_widget.bind("<Button-3>", lambda event: self.show_report_context_menu(event, tree_widget, context_menu))

    def show_report_context_menu(self, event, tree_widget, context_menu):
        """
        Показывает контекстное меню при правом клике в окне отчета
        
        Args:
            event: Событие клика
            tree_widget: Виджет Treeview
            context_menu: Контекстное меню
        """
        item = tree_widget.identify_row(event.y)
        if item:
            # Выделяем строку под курсором
            tree_widget.selection_set(item)
            # Показываем контекстное меню
            context_menu.post(event.x_root, event.y_root)

    def open_file_from_tree(self, event, tree_widget):
        """
        Обрабатывает двойной клик по элементу таблицы в окне отчета
        
        Args:
            event: Событие клика
            tree_widget: Виджет Treeview
        """
        # Получаем идентификатор выбранного элемента
        item_id = tree_widget.identify('item', event.x, event.y)
        if not item_id:
            return
        
        # Получаем значения для выбранного элемента
        values = tree_widget.item(item_id, 'values')
        if not values or len(values) < 4:
            return
        
        # Путь к файлу находится в 4-м столбце (индекс 3)
        file_path = values[3]
        if file_path:
            # Проверяем, существует ли файл перед попыткой открытия
            if os.path.exists(file_path):
                success, error = open_file(file_path)
                if not success:
                    self.show_warning("Предупреждение", error)
            else:
                self.show_warning("Предупреждение", f"Файл не найден:\n{file_path}")

    def open_file_from_tree_selection(self, tree_widget):
        """
        Открывает выбранный файл из контекстного меню в окне отчета
        
        Args:
            tree_widget: Виджет Treeview
        """
        selection = tree_widget.selection()
        if selection:
            values = tree_widget.item(selection[0], 'values')
            file_path = values[3]  # Путь к файлу в 4-м столбце
            if file_path and os.path.exists(file_path):
                success, error = open_file(file_path)
                if not success:
                    self.show_warning("Предупреждение", error)
            else:
                self.show_warning("Предупреждение", f"Файл не найден:\n{file_path}")

    def open_directory_from_tree_selection(self, tree_widget):
        """
        Открывает директорию, содержащую выбранный файл в окне отчета
        
        Args:
            tree_widget: Виджет Treeview
        """
        selection = tree_widget.selection()
        if selection:
            values = tree_widget.item(selection[0], 'values')
            file_path = values[3]  # Путь к файлу в 4-м столбце
            if file_path:
                directory = os.path.dirname(file_path)
                if os.path.exists(directory):
                    success, error = open_directory(directory)
                    if not success:
                        self.show_error("Ошибка", error)
                else:
                    self.show_warning("Предупреждение", f"Директория не найдена:\n{directory}")

    def copy_path_from_tree_selection(self, tree_widget):
        """
        Копирует путь к файлу в буфер обмена из окна отчета
        
        Args:
            tree_widget: Виджет Treeview
        """
        selection = tree_widget.selection()
        if selection:
            values = tree_widget.item(selection[0], 'values')
            file_path = values[3]  # Путь к файлу в 4-м столбце
            if file_path:
                self.root.clipboard_clear()
                self.root.clipboard_append(file_path)
    
    def init_variables(self):
        """Инициализирует переменные приложения"""
        # Переменные путей
        self.selected_path = tk.StringVar()
        self.output_path = tk.StringVar()
        
        # Статус и прогресс
        self.status_text = tk.StringVar()
        self.status_text.set("Готов к работе")
        self.current_file = tk.StringVar()
        self.current_file.set("")
        self.progress_value = tk.DoubleVar()
        self.progress_value.set(0)
        
        # Настройки типов файлов
        self.check_docx = tk.BooleanVar(value=True)
        self.check_doc = tk.BooleanVar(value=True)
        self.check_docm = tk.BooleanVar(value=True)
        self.check_xlsx = tk.BooleanVar(value=True)
        self.check_xls = tk.BooleanVar(value=True)
        self.check_xlsm = tk.BooleanVar(value=True)
        
        # Состояние проверки
        self.is_checking = False
        self.stop_requested = False
        
        # Опция пропуска больших файлов
        self.skip_large_files = tk.BooleanVar(value=True)
        
        # Счетчики файлов
        self.total_files_var = tk.StringVar(value="0")
        self.remaining_files_var = tk.StringVar(value="0")
        
        # Определяем оптимальное значение потоков по умолчанию
        default_threads = min(8, max(1, int(os.cpu_count() * 0.75)) if os.cpu_count() else 4)
        self.max_threads = tk.IntVar(value=default_threads)
        
        # Результаты проверки
        self.results = []
        
        # Переменные для поиска значений в документах
        self.enable_value_search = tk.BooleanVar(value=False)  # По умолчанию отключено
        self.search_values = tk.StringVar(value='"2024", "Предоставлено ", "Утверждено"')  # Примерные значения для поиска
        
    def setup_context_menu(self):
        """Инициализирует контекстное меню"""
        self.ui_builder.setup_context_menu()
    
    def show_context_menu(self, event):
        """Показывает контекстное меню при правом клике"""
        item = self.results_tree.identify_row(event.y)
        if item:
            # Выделяем строку под курсором
            self.results_tree.selection_set(item)
            # Показываем контекстное меню
            self.context_menu.post(event.x_root, event.y_root)
    
    def browse_path(self):
        """Открывает диалог выбора файла или папки"""
        # Спрашиваем пользователя, что он хочет выбрать
        choice = messagebox.askquestion("Выбор", "Хотите выбрать папку?\n\nНажмите 'Да' для выбора папки, 'Нет' для выбора файлов")
        
        if choice == 'yes':
            # Выбор папки
            path = filedialog.askdirectory(title="Выберите папку")
            if path:
                # Нормализация пути
                normalized_path = normalize_path(path)
                self.selected_path.set(normalized_path)
        else:
            # Формируем строку фильтра на основе выбранных типов файлов
            filter_extensions = []
            
            # Добавляем выбранные расширения Word
            word_exts = []
            if self.check_docx.get():
                word_exts.append("*.docx")
            if self.check_doc.get():
                word_exts.append("*.doc")
            if self.check_docm.get():
                word_exts.append("*.docm")
                
            # Добавляем выбранные расширения Excel
            excel_exts = []
            if self.check_xlsx.get():
                excel_exts.append("*.xlsx")
            if self.check_xls.get():
                excel_exts.append("*.xls")
            if self.check_xlsm.get():
                excel_exts.append("*.xlsm")
            
            # Формируем список фильтров для диалога выбора файлов
            if word_exts or excel_exts:
                all_exts = word_exts + excel_exts
                if all_exts:
                    filter_extensions.append(("Все поддерживаемые типы", ";".join(all_exts)))
                
                if word_exts:
                    filter_extensions.append(("Word Documents", ";".join(word_exts)))
                
                if excel_exts:
                    filter_extensions.append(("Excel Files", ";".join(excel_exts)))
                    
                filter_extensions.append(("All Files", "*.*"))
            else:
                # Если ничего не выбрано, показываем все типы
                filter_extensions = [
                    ("Documents", "*.docx;*.doc;*.docm;*.xlsx;*.xls;*.xlsm"),
                    ("Word Documents", "*.docx;*.doc;*.docm"),
                    ("Excel Files", "*.xlsx;*.xls;*.xlsm"),
                    ("All Files", "*.*")
                ]
            
            # Выбор нескольких файлов
            files = filedialog.askopenfilenames(
                title="Выберите файлы",
                filetypes=filter_extensions
            )
            
            if files:
                # Нормализация путей и сохранение списка файлов разделенных ||| (чтобы обрабатывать пути с пробелами)
                normalized_files = [normalize_path(f) for f in files]
                self.selected_path.set("|||".join(normalized_files))
    
    def get_extensions_to_check(self):
        """Возвращает список расширений файлов, которые нужно проверить"""
        extensions = []
        
        # Добавляем выбранные расширения Word
        if self.check_docx.get():
            extensions.append('.docx')
        if self.check_doc.get():
            extensions.append('.doc')
        if self.check_docm.get():
            extensions.append('.docm')
            
        # Добавляем выбранные расширения Excel
        if self.check_xlsx.get():
            extensions.append('.xlsx')
        if self.check_xls.get():
            extensions.append('.xls')
        if self.check_xlsm.get():
            extensions.append('.xlsm')
        
        return extensions
    
    def browse_output_path(self):
        """Открывает диалог выбора пути для сохранения отчета"""
        # Запрос пути для сохранения отчета
        file_path = filedialog.asksaveasfilename(
            title="Укажите файл для сохранения отчета",
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")]
        )
        
        if file_path:
            # Нормализуем путь к файлу
            normalized_path = normalize_path(file_path)
            self.output_path.set(normalized_path)
            
            # После выбора нового пути отчета, проверяем существующий файл
            # и определяем текущий номер запуска
            self.report_manager.load_run_id_from_report()
    
    def clear_results(self):
        """Очищает результаты проверки"""
        # Проверяем, не идет ли сейчас проверка
        if self.is_checking:
            return  # Не очищаем результаты во время проверки
        
        # Очистка таблицы результатов
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Очистка списка результатов
        self.results = []
        
        # Сбрасываем счетчики файлов
        self.total_files_var.set("0")
        self.remaining_files_var.set("0")
        
        # Обновление статуса
        self.status_text.set("Результаты очищены")
        self.current_file.set("")
        self.progress_value.set(0)
    
    def open_selected_file(self):
        """Открывает выбранный файл из контекстного меню"""
        selection = self.results_tree.selection()
        if selection:
            values = self.results_tree.item(selection[0], 'values')
            file_path = values[3]  # Путь к файлу в 4-м столбце
            if file_path and os.path.exists(file_path):
                success, error = open_file(file_path)
                if not success:
                    self.show_warning("Предупреждение", error)
            else:
                self.show_warning("Предупреждение", f"Файл не найден:\n{file_path}")
    
    def open_file_directory(self):
        """Открывает директорию, содержащую выбранный файл"""
        selection = self.results_tree.selection()
        if selection:
            values = self.results_tree.item(selection[0], 'values')
            file_path = values[3]  # Путь к файлу в 4-м столбце
            if file_path:
                directory = os.path.dirname(file_path)
                if os.path.exists(directory):
                    success, error = open_directory(directory)
                    if not success:
                        self.show_error("Ошибка", error)
                else:
                    self.show_warning("Предупреждение", f"Директория не найдена:\n{directory}")
    
    def copy_file_path(self):
        """Копирует путь к файлу в буфер обмена"""
        selection = self.results_tree.selection()
        if selection:
            values = self.results_tree.item(selection[0], 'values')
            file_path = values[3]  # Путь к файлу в 4-м столбце
            if file_path:
                self.root.clipboard_clear()
                self.root.clipboard_append(file_path)
    
    def on_item_double_click(self, event):
        """Обрабатывает двойной клик по элементу таблицы"""
        # Получаем идентификатор выбранного элемента
        item_id = self.results_tree.identify('item', event.x, event.y)
        if not item_id:
            return
        
        # Получаем значения для выбранного элемента
        values = self.results_tree.item(item_id, 'values')
        if not values or len(values) < 4:
            return
        
        # Путь к файлу находится в 4-м столбце (индекс 3)
        file_path = values[3]
        if file_path:
            # Проверяем, существует ли файл перед попыткой открытия
            if os.path.exists(file_path):
                success, error = open_file(file_path)
                if not success:
                    self.show_warning("Предупреждение", error)
            else:
                self.show_warning("Предупреждение", f"Файл не найден:\n{file_path}")
    
    def start_check(self):
        """Запускает процесс проверки документов"""
        # Если проверка уже идет, просто возвращаемся
        if self.is_checking:
            return
        
        path = self.selected_path.get()
        
        if not path:
            self.show_error("Ошибка", "Необходимо выбрать файл или папку")
            return
        
        # Перезагружаем данные из отчета для гарантии актуальности
        self.report_manager.load_run_id_from_report()
        
        # Очищаем результаты предыдущей проверки в интерфейсе
        self.clear_results()
        
        # Сбрасываем список результатов (текущего запуска)
        self.results = []
        
        # Увеличиваем порядковый номер запуска
        self.report_manager.current_run_id += 1
        
        # Обновляем отображение текущего номера запуска
        self.run_id_label.config(text=str(self.report_manager.current_run_id))
        
        # Предварительно подсчитываем количество файлов для отображения
        threading.Thread(target=self.count_files_to_process, args=(path,), daemon=True).start()
    
    def count_files_to_process(self, path):
        """Предварительный подсчет файлов для корректного отображения"""
        try:
            # Получаем список расширений, которые нужно проверить
            extensions_to_check = self.get_extensions_to_check()
            
            if not extensions_to_check:
                self.status_text.set("Не выбрано ни одного типа файлов для проверки")
                self.root.after(0, lambda: self.show_warning("Предупреждение", 
                                                  "Не выбрано ни одного типа файлов для проверки.\n"
                                                  "Пожалуйста, выберите хотя бы один тип файла."))
                return
            
            # Для отображения статуса
            self.status_text.set("Подсчет файлов...")
            
            # Проверяем, не список ли это файлов (с разделителем |||)
            if "|||" in path:
                files = path.split("|||")
                # Фильтруем файлы по выбранным расширениям
                files = [f for f in files if os.path.splitext(f)[1].lower() in extensions_to_check]
            elif os.path.isfile(path):
                # Проверяем, соответствует ли расширение файла выбранным типам
                if os.path.splitext(path)[1].lower() in extensions_to_check:
                    files = [path]
                else:
                    files = []
            else:  # Папка
                files = []
                for root, _, filenames in os.walk(path):
                    for filename in filenames:
                        file_ext = os.path.splitext(filename)[1].lower()
                        if file_ext in extensions_to_check:
                            # Нормализуем пути
                            file_path = normalize_path(os.path.join(root, filename))
                            files.append(file_path)
            
            # Пропускаем временные файлы
            files = [f for f in files if not os.path.basename(f).startswith("~$")]
            
            # Обновляем отображение количества файлов
            total_files = len(files)
            self.root.after(0, lambda count=total_files: self.update_file_counts(count))
            
            # Если нет файлов для проверки, выводим сообщение
            if not files:
                self.status_text.set("Нет файлов для проверки")
                self.root.after(0, lambda: self.show_info("Информация", 
                                                "В указанном пути не найдено файлов выбранных типов."))
                return
            
            # Запускаем фактическую проверку
            self.root.after(0, lambda: self.start_actual_check(path))
            
        except Exception as e:
            self.status_text.set("Ошибка при подсчете файлов")
            error_message = str(e)
            self.root.after(0, lambda error=error_message: self.show_error("Ошибка", f"Произошла ошибка при подсчете файлов: {error}"))
    
    def start_actual_check(self, path):
        """Запускает фактическую проверку файлов после подсчета их количества"""
        # Устанавливаем флаги проверки
        self.is_checking = True
        self.stop_requested = False
        
        # Изменяем текст и команду кнопки
        self.action_button.config(text="Остановить проверку", command=self.stop_check)
        
        # Запуск проверки в отдельном потоке, чтобы не блокировать интерфейс
        threading.Thread(target=self.process_path, args=(path,), daemon=True).start()
    
    def update_file_counts(self, total_count):
        """Обновляет счетчики количества файлов"""
        self.total_files_var.set(str(total_count))
        self.remaining_files_var.set(str(total_count))
        
        # Обновляем статус
        self.status_text.set(f"Найдено файлов: {total_count}")
    
    def stop_check(self):
        """Останавливает процесс проверки"""
        if not self.is_checking:
            return
        
        # Устанавливаем флаг запроса на остановку
        self.stop_requested = True
        self.status_text.set("Останавливается...")
    
    def update_results_tree(self, result):
        """Обновляет дерево результатов новым результатом"""
        # Определение номера строки
        row_num = len(self.results_tree.get_children()) + 1
        
        # Определение тега для строки (цвета)
        tag = 'passed' if result['result'] == "Пройден" else 'failed'
        
        # Нормализуем путь к файлу 
        normalized_path = normalize_path(result['file_path'])
        result['file_path'] = normalized_path
        
        # Добавляем в результат номер запуска
        result['run_id'] = self.report_manager.current_run_id
        
        # Вставка строки в таблицу
        item_id = self.results_tree.insert(
            '', 'end',
            values=(
                row_num,
                result['file_name'],
                result['file_type'],
                normalized_path,
                result['result'],
                result['comment']
            ),
            tags=(tag,)
        )
    
    def update_progress(self, progress_value, remaining_files):
        """Обновляет прогресс и индикаторы количества файлов"""
        self.progress_value.set(progress_value)
        self.remaining_files_var.set(str(remaining_files))
    
    def finalize_check(self, save_results=True):
        """Финализирует процесс проверки, восстанавливая интерфейс"""
        # Сбрасываем флаги проверки
        self.is_checking = False
        self.stop_requested = False
        
        # Возвращаем кнопке исходный текст и команду
        self.action_button.config(text="Начать проверку", command=self.start_check)
        
        # Сохраняем текущие настройки
        self.config_manager.save_settings()
    
    def process_path(self, path):
        """Обрабатывает указанный путь (файл или папку)"""
        self.status_text.set("Идет проверка...")
        self.progress_value.set(0)
        
        try:
            # Получаем список расширений, которые нужно проверить
            extensions_to_check = self.get_extensions_to_check()
            
            if not extensions_to_check:
                self.status_text.set("Не выбрано ни одного типа файлов для проверки")
                self.root.after(0, lambda: self.show_warning("Предупреждение", 
                                                  "Не выбрано ни одного типа файлов для проверки.\n"
                                                  "Пожалуйста, выберите хотя бы один тип файла."))
                # Сбрасываем состояние проверки и восстанавливаем кнопку
                self.finalize_check(save_results=False)
                return
            
            # Проверяем, не список ли это файлов (с разделителем |||)
            if "|||" in path:
                files = path.split("|||")
                # Фильтруем файлы по выбранным расширениям
                files = [f for f in files if os.path.splitext(f)[1].lower() in extensions_to_check]
            # Определяем, это файл или папка
            elif os.path.isfile(path):
                # Проверяем, соответствует ли расширение файла выбранным типам
                if os.path.splitext(path)[1].lower() in extensions_to_check:
                    files = [path]
                else:
                    files = []
            else:  # Папка
                files = []
                for root, _, filenames in os.walk(path):
                    for filename in filenames:
                        file_ext = os.path.splitext(filename)[1].lower()
                        if file_ext in extensions_to_check:
                            # Нормализуем пути
                            file_path = normalize_path(os.path.join(root, filename))
                            files.append(file_path)
            
            # Пропускаем временные файлы
            files = [f for f in files if not os.path.basename(f).startswith("~$")]
            
            # Если нет файлов для проверки, выводим сообщение
            if not files:
                self.status_text.set("Нет файлов для проверки")
                self.root.after(0, lambda: self.show_info("Информация", 
                                                "В указанном пути не найдено файлов выбранных типов."))
                # Сбрасываем состояние проверки и восстанавливаем кнопку
                self.finalize_check(save_results=False)
                return
            
            # Нормализуем все оставшиеся пути
            files = [normalize_path(f) for f in files]
            
            # Обновляем отображение количества файлов
            total_files = len(files)
            self.total_files_var.set(str(total_files))
            self.remaining_files_var.set(str(total_files))
            
            # Многопоточная обработка файлов
            import concurrent.futures
            from queue import Queue
            
            # Очередь для результатов обработки
            result_queue = Queue()
            # Счетчик обработанных файлов для обновления прогресса
            processed_files_counter = [0]
            
            # Защищаем доступ к счетчику с помощью мьютекса
            counter_lock = threading.Lock()
            
            # Функция для обработки одного файла в отдельном потоке
            def process_single_file(file_index, file_path):
                # Проверяем запрос на остановку
                if self.stop_requested:
                    return None
                    
                try:
                    # Получаем информацию о файле
                    file_name = os.path.basename(file_path)
                    
                    # Обновляем информацию о текущем файле в UI
                    self.root.after(0, lambda: self.current_file.set(file_name))
                    
                    # Проверяем файл
                    result = self.check_file(file_path, file_name)
                    
                    # Обновляем счетчик и прогресс-бар
                    with counter_lock:
                        processed_files_counter[0] += 1
                        progress = (processed_files_counter[0] / total_files) * 100
                        remaining = total_files - processed_files_counter[0]
                        self.root.after(0, lambda p=progress, r=remaining: self.update_progress(p, r))
                    
                    # Добавляем результат в очередь
                    result_queue.put((file_index, result))
                    
                    return result
                except Exception as e:
                    # В случае ошибки создаем запись о ней
                    error_result = {
                        'file_name': os.path.basename(file_path),
                        'file_type': get_file_type(file_path),
                        'file_path': file_path,
                        'result': "Ошибка",
                        'comment': f"Ошибка проверки: {str(e)}"
                    }
                    
                    # Обновляем счетчик и прогресс-бар
                    with counter_lock:
                        processed_files_counter[0] += 1
                        progress = (processed_files_counter[0] / total_files) * 100
                        remaining = total_files - processed_files_counter[0]
                        self.root.after(0, lambda p=progress, r=remaining: self.update_progress(p, r))
                    
                    # Добавляем результат ошибки в очередь
                    result_queue.put((file_index, error_result))
                    return error_result
            
            # Определяем оптимальное количество потоков из настроек пользователя
            max_workers = self.max_threads.get()
            
            # Создаем пул потоков и начинаем обработку
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Запускаем обработку файлов
                future_to_file = {
                    executor.submit(process_single_file, i, file_path): (i, file_path) 
                    for i, file_path in enumerate(files)
                }
                
                # Отслеживаем завершение задач и добавляем результаты
                completed_results = []
                
                # Таймер для обновления UI
                last_ui_update = time.time()
                
                # Периодически проверяем результаты и обновляем UI
                while future_to_file:
                    # Проверяем завершенные задачи
                    done, not_done = concurrent.futures.wait(
                        future_to_file.keys(),
                        timeout=0.1,  # Небольшой тайм-аут для проверки остановки
                        return_when=concurrent.futures.FIRST_COMPLETED
                    )
                    
                    # Если есть завершенные задачи, обрабатываем их
                    for future in done:
                        # Удаляем задачу из списка ожидания
                        file_index, file_path = future_to_file.pop(future)
                        
                        try:
                            # Получаем результат задачи
                            result = future.result()
                            if result:
                                completed_results.append(result)
                        except Exception as e:
                            # В случае необработанного исключения, создаем запись об ошибке
                            error_result = {
                                'file_name': os.path.basename(file_path),
                                'file_type': get_file_type(file_path),
                                'file_path': file_path,
                                'result': "Ошибка",
                                'comment': f"Непредвиденная ошибка: {str(e)}"
                            }
                            completed_results.append(error_result)
                            self.root.after(0, lambda r=error_result: self.update_results_tree(r))
                    
                    # Проверяем, не запрошена ли остановка
                    if self.stop_requested:
                        # Отменяем все незавершенные задачи
                        for future in list(future_to_file.keys()):
                            future.cancel()
                        break
                    
                    # Обновляем UI каждые 200ms
                    current_time = time.time()
                    if current_time - last_ui_update > 0.2:
                        last_ui_update = current_time
                        
                        # Получаем все результаты из очереди и обновляем UI
                        while not result_queue.empty():
                            _, result = result_queue.get()
                            self.results.append(result)
                            self.root.after(0, lambda r=result: self.update_results_tree(r))
                        
                        # Обновляем интерфейс
                        self.root.update()
                
                # Получаем оставшиеся результаты из очереди
                while not result_queue.empty():
                    _, result = result_queue.get()
                    self.results.append(result)
                    self.root.after(0, lambda r=result: self.update_results_tree(r))
            
            # Обновляем прогресс-бар до конечного состояния
            if self.stop_requested:
                # Если остановлено пользователем, устанавливаем прогресс в соответствии с количеством обработанных файлов
                self.progress_value.set((processed_files_counter[0] / total_files) * 100)
                # Обновляем индикатор оставшихся файлов
                self.remaining_files_var.set(str(total_files - processed_files_counter[0]))
            else:
                # Если завершено полностью, устанавливаем 100%
                self.progress_value.set(100)
                # Обновляем индикатор оставшихся файлов
                self.remaining_files_var.set("0")
            
            # Сохранение результатов в Excel только если есть что сохранить
            if self.results:
                self.report_manager.save_results_to_excel(self.results)
            
            # Обновляем статус и очищаем текущий файл
            if self.stop_requested:
                status_message = "Проверка остановлена пользователем"
                completion_message = f"Проверка остановлена. Проверено {processed_files_counter[0]} из {total_files} файлов."
            else:
                status_message = "Проверка завершена"
                completion_message = "Проверка документов завершена"
            
            self.status_text.set(status_message)
            self.current_file.set("")
            
            # Финализация проверки (восстановление кнопки, сброс флагов)
            self.finalize_check(save_results=True)
            
            # Сообщение о завершении
            self.root.after(0, lambda: self.show_info("Завершено", completion_message))
            
        except Exception as e:
            self.status_text.set("Ошибка")
            # Передаем 'e' в качестве аргумента лямбда-функции
            error_message = str(e)
            self.root.after(0, lambda error=error_message: self.show_error("Ошибка", f"Произошла ошибка: {error}"))
            # Финализация проверки при ошибке
            self.finalize_check(save_results=len(self.results) > 0)
    
    def check_file(self, file_path, file_name):
        """
        Проверяет файл в соответствии с его типом.
        
        Args:
            file_path (str): Путь к файлу
            file_name (str): Имя файла
                
        Returns:
            dict: Результат проверки
        """
        file_type = get_file_type(file_path)
        
        # Проверка, не заблокирован ли файл
        if is_locked_file(file_path):
            return {
                'file_name': file_name,
                'file_type': file_type,
                'file_path': file_path,
                'result': "Ошибка",
                'comment': "Файл заблокирован другим процессом"
            }
        
        # Определяем категорию размера файла
        size_category = detect_file_size_category(file_path)
        
        # Добавляем размер в информацию о файле для логирования
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        file_size_str = f"{file_size_mb:.2f} МБ"
        
        # При очень больших файлах (>100 МБ) и если выбрана опция пропуска больших файлов
        if size_category == "very_large" and self.skip_large_files.get():
            return {
                'file_name': file_name,
                'file_type': file_type,
                'file_path': file_path,
                'result': "Пропущен",
                'comment': f"Файл слишком большой ({file_size_str}). Пропущен согласно настройкам."
            }
        
        # Обработка параметров поиска значений
        enable_search = self.enable_value_search.get()
        search_values = []
        
        if enable_search:
            try:
                # Парсим значения из строки, разделенные запятыми и в кавычках
                values_str = self.search_values.get().strip()
                if values_str:
                    import re
                    # Ищем строки в двойных кавычках
                    pattern = r'"([^"]*)"'
                    matches = re.findall(pattern, values_str)
                    
                    # Добавляем найденные значения в список
                    if matches:
                        search_values = matches
                    else:
                        # Если не удалось найти строки в кавычках, используем запятую как разделитель
                        search_values = [val.strip() for val in values_str.split(',') if val.strip()]
            except Exception as e:
                print(f"Ошибка при обработке значений для поиска: {str(e)}")
        
        # Проверяем файл в соответствии с его типом
        if file_type == "Word":
            return check_word_file(file_path, file_name, enable_search, search_values)
        elif file_type == "Excel":
            return check_excel_file(file_path, file_name, enable_search, search_values)
        else:
            return {
                'file_name': file_name,
                'file_type': "Неизвестный",
                'file_path': file_path,
                'result': "Ошибка",
                'comment': "Неподдерживаемый тип файла"
            }
    
    # Вспомогательные методы для отображения сообщений
    def show_error(self, title, message):
        """Показывает сообщение об ошибке"""
        messagebox.showerror(title, message)
    
    def show_warning(self, title, message):
        """Показывает предупреждение"""
        messagebox.showwarning(title, message)
    
    def show_info(self, title, message):
        """Показывает информационное сообщение"""
        messagebox.showinfo(title, message)

    def save_report(self):
        """
        Сохраняет отчет о проверке в выбранный формат
        """
        # Получаем формат отчета
        if hasattr(self, 'report_format'):
            report_format = self.report_format.get()
        else:
            report_format = "xlsx"  # по умолчанию
        
        # Сохраняем отчет, используя менеджер отчетов
        if hasattr(self, 'report_manager') and hasattr(self.report_manager, 'save_report'):
            self.report_manager.save_report(format=report_format)
        else:
            from tkinter import messagebox
            messagebox.showinfo("Информация", f"Отчет будет сохранен в формате {report_format}")

    def stop_check(self):
        """
        Останавливает текущую проверку
        """
        # Здесь должен быть код для остановки проверки
        # Например, установка флага для остановки потоков
        self.status_text.set("Проверка остановлена")
        
        # Обновляем состояние кнопок
        if hasattr(self, 'ui_builder') and hasattr(self.ui_builder, 'toolbar_builder'):
            self.ui_builder.toolbar_builder.update_buttons_for_check_completed()
        
        # Обновляем кнопки в верхней панели
        if hasattr(self, 'stop_button'):
            self.stop_button.config(state=tk.DISABLED)
        if hasattr(self, 'action_button'):
            self.action_button.config(state=tk.NORMAL)

    def export_results(self, format=None):
        """
        Экспортирует результаты в выбранный формат
        """
        # Если формат не указан, используем формат из настроек
        if format is None:
            if hasattr(self, 'report_format'):
                format = self.report_format.get()
            else:
                format = "xlsx"  # по умолчанию
        
        # Экспортируем результаты
        from tkinter import filedialog, messagebox
        
        # Запрашиваем путь для сохранения
        filetypes = []
        default_extension = ""
        
        if format == "xlsx":
            filetypes = [("Excel файлы", "*.xlsx")]
            default_extension = ".xlsx"
        elif format == "csv":
            filetypes = [("CSV файлы", "*.csv")]
            default_extension = ".csv"
        elif format == "html":
            filetypes = [("HTML файлы", "*.html")]
            default_extension = ".html"
        elif format == "json":
            filetypes = [("JSON файлы", "*.json")]
            default_extension = ".json"
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=default_extension,
            filetypes=filetypes,
            title="Сохранить отчет как"
        )
        
        if filepath:
            # В реальном приложении здесь будет код для экспорта
            messagebox.showinfo("Экспорт", f"Отчет экспортирован в {filepath}")

    def copy_row_data(self):
        """
        Копирует данные выбранной строки в буфер обмена
        """
        if not hasattr(self, 'results_tree'):
            return
            
        # Получаем выбранные элементы
        selected_items = self.results_tree.selection()
        
        if not selected_items:
            return
            
        # Получаем данные первого выбранного элемента
        item = selected_items[0]
        values = self.results_tree.item(item, "values")
        
        # Формируем строку для копирования
        row_text = "\t".join([str(val) for val in values])
        
        # Копируем в буфер обмена
        self.root.clipboard_clear()
        self.root.clipboard_append(row_text)