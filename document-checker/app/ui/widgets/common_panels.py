#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import datetime

class PanelsBuilder:
    """
    Улучшенный класс для создания общих панелей интерфейса
    """
    def __init__(self, app_instance):
        self.app = app_instance

    def create_top_panel(self):
        """Создает улучшенную верхнюю панель с выбором пути и кнопками управления"""
        top_frame = ttk.Frame(self.app.root, padding="10")
        top_frame.pack(fill=tk.X)
        
        # Создаем подфрейм для заголовка (новый элемент)
        header_frame = ttk.Frame(top_frame)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Заголовок приложения
        app_title = ttk.Label(header_frame, text="Проверка документов", 
                             font=("", 12, "bold"))
        app_title.pack(side=tk.LEFT)
        
        # Справа отображаем текущий номер запуска
        if hasattr(self.app, 'report_manager') and hasattr(self.app.report_manager, 'current_run_id'):
            run_info = ttk.Label(header_frame, 
                               text=f"Запуск #{self.app.report_manager.current_run_id}", 
                               font=("", 10))
            run_info.pack(side=tk.RIGHT)
        
        # Фрейм для выбора пути с улучшенной компоновкой
        path_frame = ttk.LabelFrame(top_frame, text="Выбор файлов", padding="5")
        path_frame.pack(fill=tk.X, pady=5)
        
        # Метка и поле ввода пути в одной строке
        path_entry_frame = ttk.Frame(path_frame)
        path_entry_frame.pack(fill=tk.X, expand=True)
        
        ttk.Label(path_entry_frame, text="Путь:").pack(side=tk.LEFT, padx=(0, 10))
        
        # Поле ввода пути с возможностью ввода и редактирования
        path_entry = ttk.Entry(path_entry_frame, textvariable=self.app.selected_path, width=50)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Кнопка выбора файла
        file_button = ttk.Button(path_entry_frame, text="Выбрать файл", 
                               command=lambda: self.app.browse_path(file_only=True), width=12)
        file_button.pack(side=tk.LEFT, padx=2)
        
        # Кнопка выбора папки
        folder_button = ttk.Button(path_entry_frame, text="Выбрать папку", 
                                 command=lambda: self.app.browse_path(file_only=False), width=12)
        folder_button.pack(side=tk.LEFT, padx=2)
        
        # Панель для кнопок управления запуском
        control_frame = ttk.Frame(top_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        # Добавляем информацию о состоянии слева
        status_frame = ttk.Frame(control_frame)
        status_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        ttk.Label(status_frame, text="Статус:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(status_frame, textvariable=self.app.status_text,
                font=("", 9, "bold")).pack(side=tk.LEFT, padx=(0, 20))
        
        # Кнопки управления
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side=tk.RIGHT)
        
        self.app.action_button = ttk.Button(button_frame, text="Начать проверку", 
                                         command=self.app.start_check, width=15)
        self.app.action_button.pack(side=tk.LEFT, padx=5)
        
        self.app.stop_button = ttk.Button(button_frame, text="Остановить", 
                                       command=self.app.stop_check, state=tk.DISABLED, width=15)
        self.app.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Создаем события для горячих клавиш
        self.app.root.bind("<F5>", lambda event: self.app.start_check())
        self.app.root.bind("<Escape>", lambda event: self.app.stop_check())
        self.app.root.bind("<Control-o>", lambda event: self.app.browse_path())

    def create_bottom_info_panel(self):
        """Создает нижнюю панель с информацией о разработчике и датой"""
        bottom_info_frame = ttk.Frame(self.app.root, padding="5")
        bottom_info_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        ttk.Label(bottom_info_frame, text="@Собственная разработка ИТРА", 
                font=("", 8, "italic"), foreground="#666666").pack(side=tk.LEFT, padx=10)
        
        current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        ttk.Label(bottom_info_frame, text=f"Текущие дата и время: {current_datetime}", 
                font=("", 8, "italic"), foreground="#666666").pack(side=tk.RIGHT, padx=10)