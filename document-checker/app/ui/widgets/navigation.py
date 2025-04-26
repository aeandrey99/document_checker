#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import tkinter as tk
from tkinter import ttk

class NavigationManager:
    """
    Улучшенный класс для управления навигацией между страницами приложения
    """
    def __init__(self, app_instance, ui_builder):
        self.app = app_instance
        self.ui_builder = ui_builder
        self.breadcrumbs = []
        self.current_page = "settings"

    def create_navigation_panel(self):
        """
        Создает панель навигации с хлебными крошками и индикаторами
        """
        nav_frame = ttk.Frame(self.app.root)
        nav_frame.pack(fill=tk.X, padx=5, pady=(5, 0))
        
        # Подфрейм для хлебных крошек
        breadcrumbs_frame = ttk.Frame(nav_frame)
        breadcrumbs_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Добавляем начальную хлебную крошку
        self.home_label = ttk.Label(breadcrumbs_frame, text="Главная", 
                                 font=("", 9, "underline"), foreground="#4285f4",
                                 cursor="hand2")
        self.home_label.pack(side=tk.LEFT)
        self.home_label.bind("<Button-1>", lambda e: self.navigate_to("home"))
        
        # Подфрейм справа для информации о последнем запуске
        info_frame = ttk.Frame(nav_frame)
        info_frame.pack(side=tk.RIGHT, padx=10)
        
        # Создаем интерактивный элемент с информацией о запуске
        ttk.Label(info_frame, text="История: ", font=("", 8)).pack(side=tk.LEFT)
        
        # Создаем список для выбора запуска
        if not hasattr(self.app, 'run_history'):
            # Список для истории запусков
            self.app.run_history = []
            current_run_id = self.app.report_manager.current_run_id if hasattr(self.app, 'report_manager') and hasattr(self.app.report_manager, 'current_run_id') else 1
            self.app.run_history.append(f"Запуск #{current_run_id}")
            
        # Переменная для хранения выбранного запуска
        if not hasattr(self.app, 'selected_run'):
            self.app.selected_run = tk.StringVar()
            self.app.selected_run.set(self.app.run_history[0])
            
        # Комбобокс для выбора запуска из истории
        run_combo = ttk.Combobox(info_frame, textvariable=self.app.selected_run, 
                               values=self.app.run_history, width=15, state="readonly")
        run_combo.pack(side=tk.LEFT)
        run_combo.bind("<<ComboboxSelected>>", self.on_run_selected)
        
        # Добавляем кнопку для просмотра истории запусков
        history_button = ttk.Button(info_frame, text="Подробнее", 
                                  command=self.show_run_history, width=10)
        history_button.pack(side=tk.LEFT, padx=5)
        
        # Создаем хлебные крошки для текущего состояния
        self.update_breadcrumbs("settings")

    def update_breadcrumbs(self, current_page):
        """
        Обновляет хлебные крошки для навигации
        """
        # Запоминаем текущую страницу
        self.current_page = current_page
        
        # Удаляем предыдущие хлебные крошки
        for widget in self.breadcrumbs:
            widget.destroy()
        self.breadcrumbs = []
        
        # Создаем пустой список для новых виджетов
        new_breadcrumbs = []
        
        # Добавляем стрелку после "Главная"
        arrow1 = ttk.Label(self.home_label.master, text=" → ")
        arrow1.pack(side=tk.LEFT)
        new_breadcrumbs.append(arrow1)
        
        # Добавляем текущую страницу
        if current_page == "settings":
            # Настройки
            settings_label = ttk.Label(self.home_label.master, text="Настройки", 
                                    font=("", 9, "bold"))
            settings_label.pack(side=tk.LEFT)
            new_breadcrumbs.append(settings_label)
            
        elif current_page == "status":
            # Страница статуса
            settings_label = ttk.Label(self.home_label.master, text="Настройки", 
                                     font=("", 9, "underline"), foreground="#4285f4",
                                     cursor="hand2")
            settings_label.pack(side=tk.LEFT)
            settings_label.bind("<Button-1>", lambda e: self.navigate_to("settings"))
            new_breadcrumbs.append(settings_label)
            
            # Стрелка после "Настройки"
            arrow2 = ttk.Label(self.home_label.master, text=" → ")
            arrow2.pack(side=tk.LEFT)
            new_breadcrumbs.append(arrow2)
            
            # Текущая страница - Статус
            status_label = ttk.Label(self.home_label.master, text="Статус и отчет", 
                                  font=("", 9, "bold"))
            status_label.pack(side=tk.LEFT)
            new_breadcrumbs.append(status_label)
            
        # Сохраняем список хлебных крошек
        self.breadcrumbs = new_breadcrumbs

    def navigate_to(self, page):
        """
        Выполняет переход на указанную страницу
        """
        if page == "home":
            # Переход на главную страницу (в данном случае - настройки)
            self.ui_builder.show_settings_page()
            self.update_breadcrumbs("settings")
        elif page == "settings":
            self.ui_builder.show_settings_page()
            self.update_breadcrumbs("settings")
        elif page == "status":
            self.ui_builder.show_status_page()
            self.update_breadcrumbs("status")

    def on_run_selected(self, event):
        """
        Обрабатывает выбор запуска из истории
        """
        selected_run = self.app.selected_run.get()
        
        # Извлекаем номер запуска из строки "Запуск #N"
        try:
            run_id = int(selected_run.split('#')[1])
            
            # Вызываем метод загрузки отчета для выбранного запуска
            if hasattr(self.app, 'load_run_report'):
                self.app.load_run_report(run_id)
            else:
                print(f"Загрузка отчета для запуска #{run_id}")
                
            # Переходим на страницу статуса
            self.navigate_to("status")
            
        except (IndexError, ValueError):
            print(f"Ошибка при обработке запуска: {selected_run}")

    def add_run_to_history(self, run_id):
        """
        Добавляет новый запуск в историю
        """
        run_entry = f"Запуск #{run_id}"
        
        if run_entry not in self.app.run_history:
            self.app.run_history.insert(0, run_entry)
            
            # Ограничиваем количество запусков в истории (например, 10)
            if len(self.app.run_history) > 10:
                self.app.run_history.pop()
                
        # Обновляем значения в комбобоксе
        for widget in self.app.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Frame):
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, ttk.Combobox) and grandchild.winfo_parent() == child.winfo_parent():
                                grandchild.config(values=self.app.run_history)
        
        # Устанавливаем текущий запуск
        self.app.selected_run.set(run_entry)

    def show_run_history(self):
        """
        Показывает подробную историю запусков
        """
        history_window = tk.Toplevel(self.app.root)
        history_window.title("История запусков")
        history_window.geometry("600x400")
        history_window.transient(self.app.root)
        history_window.grab_set()
        
        # Применяем текущую тему
        if hasattr(self.app, 'theme_manager'):
            history_window.configure(bg=self.app.theme_manager.current_theme_colors["bg"])
        
        # Создаем фрейм для списка запусков
        history_frame = ttk.Frame(history_window, padding="10")
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        ttk.Label(history_frame, text="История запусков проверки документов", 
                font=("", 12, "bold")).pack(pady=(0, 10))
        
        # Создаем фрейм для таблицы
        table_frame = ttk.Frame(history_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Создаем таблицу с историей запусков
        columns = ("№", "Дата и время", "Проверено файлов", "Успешно", "С ошибками", "Действия")
        history_tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        for col in columns:
            history_tree.heading(col, text=col)
            
        history_tree.column("№", width=40, anchor=tk.CENTER)
        history_tree.column("Дата и время", width=150)
        history_tree.column("Проверено файлов", width=120, anchor=tk.CENTER)
        history_tree.column("Успешно", width=80, anchor=tk.CENTER)
        history_tree.column("С ошибками", width=100, anchor=tk.CENTER)
        history_tree.column("Действия", width=80, anchor=tk.CENTER)
        
        # Заполняем таблицу тестовыми данными
        # В реальном приложении здесь будут данные из БД или файла
        for i, run in enumerate(self.app.run_history):
            run_id = run.split('#')[1]
            date = datetime.datetime.now() - datetime.timedelta(days=i)
            date_str = date.strftime("%d.%m.%Y %H:%M:%S")
            
            # Тестовые данные
            total = 50 - i * 5 if i < 10 else 0
            success = int(total * 0.8)
            errors = total - success
            
            # Добавляем строку
            history_tree.insert('', 0, values=(run_id, date_str, total, success, errors, "Загрузить"))
        
        # Добавляем прокрутку
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=history_tree.yview)
        history_tree.configure(yscroll=scrollbar.set)
        
        history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Обработчик двойного клика для загрузки отчета
        def on_history_double_click(event):
            item = history_tree.selection()[0]
            run_id = history_tree.item(item, "values")[0]
            
            # Закрываем окно
            history_window.destroy()
            
            # Загружаем отчет
            if hasattr(self.app, 'load_run_report'):
                self.app.load_run_report(int(run_id))
            else:
                print(f"Загрузка отчета для запуска #{run_id}")
                
            # Переходим на страницу статуса
            self.navigate_to("status")
            
            # Обновляем выбранный запуск в комбобоксе
            self.app.selected_run.set(f"Запуск #{run_id}")
            
        history_tree.bind('<Double-1>', on_history_double_click)
        
        # Панель с кнопками
        buttons_frame = ttk.Frame(history_window)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(buttons_frame, text="Загрузить выбранный", 
                 command=lambda: on_history_double_click(None), 
                 width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Удалить выбранный", 
                 command=self.delete_selected_run, 
                 width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Закрыть", 
                 command=history_window.destroy, 
                 width=15).pack(side=tk.RIGHT, padx=5)

    def delete_selected_run(self):
        """
        Удаляет выбранный запуск из истории
        """
        # В реальном приложении здесь будет удаление из БД или файла
        print(f"Удаление запуска: {self.app.selected_run.get()}")
        
        # Удаляем из списка истории
        if self.app.selected_run.get() in self.app.run_history:
            self.app.run_history.remove(self.app.selected_run.get())
            
            # Если история пуста, добавляем текущий запуск
            if not self.app.run_history:
                current_run_id = self.app.report_manager.current_run_id if hasattr(self.app, 'report_manager') and hasattr(self.app.report_manager, 'current_run_id') else 1
                self.app.run_history.append(f"Запуск #{current_run_id}")
                
            # Устанавливаем первый запуск из оставшихся
            self.app.selected_run.set(self.app.run_history[0])