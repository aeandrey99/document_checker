#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

from ..theme import apply_theme, configure_tags
from ..widgets.components.navigation import NavigationManager
from ..widgets.pages.settings_page import SettingsPageBuilder
from ..widgets.pages.status_page import StatusPageBuilder
from ..widgets.common.panels import PanelsBuilder
from ..widgets.common.utils import UIUtils

class UIBuilder:
    """
    Класс для создания и настройки элементов интерфейса приложения.
    """
    def __init__(self, app_instance):
        self.app = app_instance
        
        # Инициализируем объект утилит
        self.utils = UIUtils()
        
        # Инициализируем строителей для разных компонентов
        self.panels_builder = PanelsBuilder(app_instance)
        self.navigation_manager = NavigationManager(app_instance, self)
        self.settings_builder = SettingsPageBuilder(app_instance)
        self.status_builder = StatusPageBuilder(app_instance)
        
        # Флаг инициализации для анимаций
        self.initialized = False

    def create_widgets(self):
        """
        Создает все элементы интерфейса приложения
        """
        # Применяем тему к интерфейсу
        apply_theme(self.app.root)
        
        # Верхняя панель (всегда видима)
        self.panels_builder.create_top_panel()
        
        # Панель с кнопками переключения страниц (всегда видима)
        self.navigation_manager.create_navigation_panel()
        
        # Создаем статусную строку с подсказками
        self.panels_builder.create_status_bar()
        
        # Создаем контейнер для страницы настроек
        self.settings_page = ttk.Frame(self.app.root)
        self.settings_builder.create_settings_page(self.settings_page)
        
        # Создаем контейнер для страницы статусов и отчётов
        self.status_page = ttk.Frame(self.app.root)
        self.status_builder.create_status_page(self.status_page)
        
        # Создаем нижнюю панель с информацией о разработчике и датой (всегда видима)
        self.panels_builder.create_bottom_info_panel()
        
        # По умолчанию показываем страницу настроек
        self.show_settings_page()
        
        # Привязываем обработчик событий для результатов
        if hasattr(self.app, 'results_tree'):
            # Обработчик двойного клика
            self.app.results_tree.bind('<Double-1>', self.app.on_item_double_click)
            
            # Настраиваем контекстное меню для таблицы
            self.setup_context_menu()
            
            # Настраиваем теги для таблицы
            configure_tags(self.app.results_tree)
        
        # Настраиваем обработку изменения размера окна
        self.app.root.bind("<Configure>", self.on_window_resize)
        
        # Настраиваем горячие клавиши
        self.setup_hotkeys()
        
        # Устанавливаем флаг инициализации
        self.initialized = True

    def show_settings_page(self):
        """
        Показывает страницу настроек и скрывает страницу статусов с анимацией
        """
        # Если интерфейс еще не инициализирован, просто показываем страницу
        if not self.initialized:
            self.status_page.pack_forget()
            self.settings_page.pack(fill=tk.BOTH, expand=True, pady=0)
            return
            
        # Если статусная страница видима, скрываем её с анимацией
        if self.status_page.winfo_viewable():
            # Обновляем статусную строку
            if hasattr(self.app, 'set_status'):
                self.app.set_status("Переход на страницу настроек...")
                
            # Эффект затухания
            for alpha in range(10, 0, -1):
                self.status_page.update()  # Обновляем страницу
                self.app.root.after(10)  # Небольшая задержка
            
            # Скрываем статусную страницу
            self.status_page.pack_forget()
            
            # Показываем страницу настроек с эффектом появления
            self.settings_page.pack(fill=tk.BOTH, expand=True, pady=0)
            
            # Обновляем статусную строку
            if hasattr(self.app, 'set_status'):
                self.app.set_status("Страница настроек. Настройте параметры проверки.")

    def show_status_page(self):
        """
        Показывает страницу статусов и скрывает страницу настроек с анимацией
        """
        # Если интерфейс еще не инициализирован, просто показываем страницу
        if not self.initialized:
            self.settings_page.pack_forget()
            self.status_page.pack(fill=tk.BOTH, expand=True, pady=0)
            return
            
        # Если страница настроек видима, скрываем её с анимацией
        if self.settings_page.winfo_viewable():
            # Обновляем статусную строку
            if hasattr(self.app, 'set_status'):
                self.app.set_status("Переход на страницу статусов и отчетов...")
                
            # Эффект затухания
            for alpha in range(10, 0, -1):
                self.settings_page.update()  # Обновляем страницу
                self.app.root.after(10)  # Небольшая задержка
            
            # Скрываем страницу настроек
            self.settings_page.pack_forget()
            
            # Показываем статусную страницу с эффектом появления
            self.status_page.pack(fill=tk.BOTH, expand=True, pady=0)
            
            # Обновляем статусную строку
            if hasattr(self.app, 'set_status'):
                self.app.set_status("Страница статусов и отчетов. Здесь отображаются результаты проверки.")

    def on_window_resize(self, event):
        """
        Обрабатывает изменение размера окна
        """
        if event.widget == self.app.root:
            if hasattr(self.app, 'results_tree'):
                # Получаем новую ширину окна
                window_width = event.width
                
                # Рассчитываем ширину для колонок
                fixed_columns_width = 40 + 150 + 80 + 100  # Ширина фиксированных колонок
                scrollbar_width = 20  # Примерная ширина полосы прокрутки
                padding = 40  # Дополнительные отступы
                
                # Распределяем оставшееся пространство между колонками путь и комментарий
                remaining_width = max(300, window_width - fixed_columns_width - scrollbar_width - padding)
                path_width = int(remaining_width * 0.4)  # 40% для пути
                comment_width = int(remaining_width * 0.6)  # 60% для комментария
                
                # Обновляем ширину колонок
                self.app.results_tree.column("Путь к файлу", width=path_width)
                self.app.results_tree.column("Комментарий", width=comment_width)

    def setup_context_menu(self):
        """
        Настраивает контекстное меню для таблицы результатов
        """
        # Создаем контекстное меню
        self.app.context_menu = tk.Menu(self.app.root, tearoff=0)
        
        # Добавляем команды в меню
        self.app.context_menu.add_command(
            label="Открыть файл", 
            command=self.app.open_selected_file
        )
        
        self.app.context_menu.add_command(
            label="Открыть директорию файла", 
            command=self.app.open_file_directory
        )
        
        self.app.context_menu.add_separator()
        
        self.app.context_menu.add_command(
            label="Копировать путь", 
            command=self.app.copy_file_path
        )
        
        self.app.context_menu.add_command(
            label="Копировать результат", 
            command=self.app.copy_file_result
        )
        
        # Привязываем появление меню к правому клику
        self.app.results_tree.bind("<Button-3>", self.app.show_context_menu)

    def setup_hotkeys(self):
        """
        Настраивает горячие клавиши для основных действий
        """
        # Настраиваем горячие клавиши
        self.app.root.bind('<Control-o>', lambda event: self.app.browse_path())
        self.app.root.bind('<Control-s>', lambda event: self.app.start_check())
        self.app.root.bind('<Control-1>', lambda event: self.show_settings_page())
        self.app.root.bind('<Control-2>', lambda event: self.show_status_page())
        self.app.root.bind('<F5>', lambda event: self.app.start_check())
        self.app.root.bind('<F1>', lambda event: self.show_help())
    
    def show_help(self):
        """
        Показывает окно с помощью
        """
        help_window = tk.Toplevel(self.app.root)
        help_window.title("Справка по программе")
        help_window.geometry("600x400")
        help_window.transient(self.app.root)
        help_window.resizable(True, True)
        help_window.focus_set()
        
        # Центрируем окно справки
        self.utils.center_window(help_window, 600, 400)
        
        # Создаем заголовок
        ttk.Label(
            help_window, 
            text="Справка по использованию", 
            font=("", 14, "bold")
        ).pack(pady=10)
        
        # Создаем фрейм с прокруткой для текста справки
        frame = ttk.Frame(help_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        # Добавляем полосу прокрутки
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Создаем текстовое поле
        text = tk.Text(
            frame, 
            wrap=tk.WORD, 
            yscrollcommand=scrollbar.set,
            font=("", 10),
            padx=10,
            pady=10
        )
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text.yview)
        
        # Добавляем текст справки
        help_text = """
        Программа для проверки документов
        ================================
        
        Горячие клавиши:
        ---------------
        Ctrl+O - Выбрать папку или файл
        Ctrl+S или F5 - Начать проверку
        Ctrl+1 - Перейти на страницу настроек
        Ctrl+2 - Перейти на страницу статусов
        F1 - Показать справку
        
        Основные действия:
        ----------------
        1. Выберите папку или файл для проверки, используя кнопку "Обзор"
        2. На вкладке "Типы файлов" отметьте форматы документов для проверки
        3. Настройте дополнительные параметры на вкладке "Опции"
        4. При необходимости настройте поиск значений на соответствующей вкладке
        5. Укажите путь для сохранения отчета
        6. Нажмите кнопку "Начать проверку"
        
        Работа с результатами:
        --------------------
        • Двойной клик по файлу в таблице открывает его
        • Правый клик вызывает контекстное меню с дополнительными действиями
        • Используйте фильтры для отображения только нужных результатов
        • Нажатие на заголовок столбца сортирует таблицу по этому столбцу
        
        При возникновении проблем обратитесь к администратору или в службу поддержки.
        """
        
        text.insert(tk.END, help_text)
        text.config(state=tk.DISABLED)  # Делаем текст только для чтения
        
        # Кнопка закрытия
        ttk.Button(
            help_window, 
            text="Закрыть", 
            command=help_window.destroy
        ).pack(pady=10)