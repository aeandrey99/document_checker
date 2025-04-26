#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

class StatusPageBuilder:
    """
    Класс для создания элементов на странице статуса и отчетов
    """
    def __init__(self, app_instance):
        self.app = app_instance

    def create_status_page(self, parent_frame):
        """
        Создаёт страницу со статусами, прогресс-баром и таблицей результатов
        """
        self.create_status_panel(parent_frame)
        self.create_progress_bar(parent_frame)
        self.create_results_table(parent_frame)
        
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