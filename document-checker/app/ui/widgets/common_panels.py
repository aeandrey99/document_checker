#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import datetime

class PanelsBuilder:
    """
    Класс для создания общих панелей интерфейса
    """
    def __init__(self, app_instance):
        self.app = app_instance

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

    def create_bottom_info_panel(self):
        """Создает нижнюю панель с информацией о разработчике и датой"""
        bottom_info_frame = ttk.Frame(self.app.root, padding="5")
        bottom_info_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        ttk.Label(bottom_info_frame, text="@Собственная разработка ИТРА", 
                font=("", 8, "italic"), foreground="#666666").pack(side=tk.LEFT, padx=10)
        
        current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        ttk.Label(bottom_info_frame, text=f"Текущие дата и время: {current_datetime}", 
                font=("", 8, "italic"), foreground="#666666").pack(side=tk.RIGHT, padx=10)