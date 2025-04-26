#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

class ToolbarBuilder:
    """
    Класс для создания панели инструментов
    """
    def __init__(self, app_instance):
        self.app = app_instance
        self.toolbar_buttons = {}

    def create_toolbar(self):
        """
        Создает панель инструментов с кнопками быстрого доступа
        """
        toolbar_frame = ttk.Frame(self.app.root)
        toolbar_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Создаем кнопки для общих действий
        self._add_button(toolbar_frame, "Открыть", self.app.browse_path, "open")
        self._add_button(toolbar_frame, "Начать", self.app.start_check, "start")
        self._add_button(toolbar_frame, "Остановить", self.app.stop_check, "stop")
        
        # Вертикальный разделитель
        ttk.Separator(toolbar_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)
        
        # Кнопки для работы с отчетами
        self._add_button(toolbar_frame, "Сохранить отчет", self.app.save_report, "save")
        self._add_button(toolbar_frame, "Экспорт", self.app.export_results, "export")
        
        # Разделитель
        ttk.Separator(toolbar_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)
        
        # Кнопки для настройки
        self._add_button(toolbar_frame, "Настройки", self.app.ui_builder.show_settings_page, "settings")
        self._add_button(toolbar_frame, "Помощь", self.show_help, "help")
        
        # Поиск (справа)
        search_frame = ttk.Frame(toolbar_frame)
        search_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Label(search_frame, text="Поиск:").pack(side=tk.LEFT)
        
        # Создаем переменную для поиска, если её еще нет
        if not hasattr(self.app, 'search_query'):
            self.app.search_query = tk.StringVar()
        
        search_entry = ttk.Entry(search_frame, textvariable=self.app.search_query, width=20)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Добавляем кнопку поиска
        search_button = ttk.Button(search_frame, text="Найти", command=self.search_in_results)
        search_button.pack(side=tk.LEFT)
        
        # Обработчик нажатия Enter в поле поиска
        search_entry.bind("<Return>", lambda event: self.search_in_results())
        
        # Настраиваем начальное состояние кнопок
        self.toolbar_buttons["stop"].config(state=tk.DISABLED)
        
    def _add_button(self, parent, text, command, name):
        """
        Добавляет кнопку на панель инструментов и сохраняет её для последующего доступа
        """
        button = ttk.Button(parent, text=text, command=command, width=10)
        button.pack(side=tk.LEFT, padx=2)
        self.toolbar_buttons[name] = button
        return button
    
    def update_for_settings_page(self):
        """
        Обновляет состояние кнопок для страницы настроек
        """
        # На странице настроек кнопки работы с отчетами не нужны
        if "export" in self.toolbar_buttons:
            self.toolbar_buttons["export"].config(state=tk.DISABLED)
        if "save" in self.toolbar_buttons:
            self.toolbar_buttons["save"].config(state=tk.DISABLED)
    
    def update_for_status_page(self):
        """
        Обновляет состояние кнопок для страницы статуса
        """
        # На странице статуса включаем кнопки работы с отчетами
        if "export" in self.toolbar_buttons:
            self.toolbar_buttons["export"].config(state=tk.NORMAL)
        if "save" in self.toolbar_buttons:
            self.toolbar_buttons["save"].config(state=tk.NORMAL)
    
    def update_buttons_for_check_started(self):
        """
        Обновляет состояние кнопок при запуске проверки
        """
        self.toolbar_buttons["start"].config(state=tk.DISABLED)
        self.toolbar_buttons["stop"].config(state=tk.NORMAL)
        self.toolbar_buttons["open"].config(state=tk.DISABLED)
        self.toolbar_buttons["settings"].config(state=tk.DISABLED)
    
    def update_buttons_for_check_completed(self):
        """
        Обновляет состояние кнопок при завершении проверки
        """
        self.toolbar_buttons["start"].config(state=tk.NORMAL)
        self.toolbar_buttons["stop"].config(state=tk.DISABLED)
        self.toolbar_buttons["open"].config(state=tk.NORMAL)
        self.toolbar_buttons["settings"].config(state=tk.NORMAL)
    
    def show_help(self):
        """
        Показывает окно справки
        """
        help_window = tk.Toplevel(self.app.root)
        help_window.title("Справка")
        help_window.geometry("500x400")
        help_window.transient(self.app.root)
        help_window.grab_set()
        
        # Применяем текущую тему
        if hasattr(self.app, 'theme_manager'):
            help_window.configure(bg=self.app.theme_manager.current_theme_colors["bg"])
        
        # Создаем текстовое поле с прокруткой
        help_frame = ttk.Frame(help_window, padding="10")
        help_frame.pack(fill=tk.BOTH, expand=True)
        
        help_text = tk.Text(help_frame, wrap=tk.WORD)
        help_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(help_frame, orient=tk.VERTICAL, command=help_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        help_text.configure(yscrollcommand=scrollbar.set)
        
        # Заполняем текст справки
        help_content = """
        Справка по использованию программы проверки документов
        
        1. Начало работы
           - Выберите папку или файл для проверки
           - Настройте параметры проверки на вкладке "Настройки"
           - Нажмите кнопку "Начать проверку" для запуска
        
        2. Настройки
           - Выберите типы файлов для проверки
           - Настройте дополнительные параметры
           - Укажите путь для сохранения отчета
        
        3. Работа с результатами
           - Все результаты проверки отображаются в таблице
           - Дважды щелкните по строке, чтобы открыть соответствующий файл
           - Используйте контекстное меню для дополнительных действий
           - Экспортируйте результаты через меню или панель инструментов
        
        4. Горячие клавиши
           - Ctrl+O: Выбрать файл/папку
           - F5: Начать проверку
           - Esc: Остановить проверку
           - Ctrl+S: Сохранить отчет
           - Ctrl+F: Поиск в результатах
           
        5. Темы оформления
           - Переключение между светлой и темной темой через кнопку в статусной строке
        
        При возникновении вопросов обращайтесь к документации или в службу поддержки.
        """
        
        help_text.insert(tk.END, help_content)
        help_text.config(state=tk.DISABLED)  # Делаем текст только для чтения
        
        # Кнопка закрытия
        close_btn = ttk.Button(help_window, text="Закрыть", command=help_window.destroy)
        close_btn.pack(pady=10)
    
    def search_in_results(self):
        """
        Выполняет поиск по результатам в таблице
        """
        if not hasattr(self.app, 'results_tree'):
            return
            
        search_text = self.app.search_query.get().lower()
        if not search_text:
            return
            
        # Сбрасываем предыдущие выделения
        for item in self.app.results_tree.get_children():
            self.app.results_tree.item(item, tags=self.app.results_tree.item(item, "tags"))
        
        # Если поисковый запрос пустой, выходим
        if not search_text:
            return
            
        # Ищем совпадения
        found_items = []
        for item in self.app.results_tree.get_children():
            # Получаем все значения в строке
            values = self.app.results_tree.item(item, "values")
            # Преобразуем в строку для поиска
            row_text = " ".join([str(val).lower() for val in values])
            
            if search_text in row_text:
                found_items.append(item)
                # Добавляем тег "найдено" для выделения строки
                current_tags = list(self.app.results_tree.item(item, "tags"))
                if "search_result" not in current_tags:
                    current_tags.append("search_result")
                self.app.results_tree.item(item, tags=current_tags)
        
        # Настраиваем тег для выделения результатов поиска
        bg_color = "#ffeb3b" if self.app.theme_manager.current_theme == "light" else "#5c4f00"
        self.app.results_tree.tag_configure('search_result', background=bg_color)
        
        # Прокручиваем к первому найденному элементу, если он есть
        if found_items:
            self.app.results_tree.see(found_items[0])
            self.app.results_tree.selection_set(found_items[0])
            
        # Обновляем статусную строку
        if hasattr(self.app, 'status_bar_label'):
            self.app.status_bar_label.config(
                text=f"Поиск: найдено {len(found_items)} совпадений" if found_items else "Поиск: нет совпадений")