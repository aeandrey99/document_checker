#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from ...theme import FONT_SMALL_BOLD
from common.tooltips import create_tooltip

class NavigationManager:
    """
    Класс для управления навигацией между страницами приложения
    """
    def __init__(self, app_instance, ui_builder):
        self.app = app_instance
        self.ui_builder = ui_builder
        self.current_page = None

    def create_navigation_panel(self):
        """
        Создает панель с кнопками для переключения между страницами
        """
        # Создаем основную рамку для навигации
        nav_frame = ttk.Frame(self.app.root, padding="5 10 5 2")
        nav_frame.pack(fill=tk.X, padx=5, pady=0)
        
        # Создаем рамку для кнопок навигации
        button_frame = ttk.Frame(nav_frame)
        button_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Кнопка для перехода на страницу настроек с иконкой
        self.settings_button = ttk.Button(
            button_frame, 
            text="Настройки ⚙", 
            command=self._show_settings_page,
            padding="10 5"
        )
        self.settings_button.pack(side=tk.LEFT, padx=5)
        create_tooltip(self.settings_button, "Перейти к настройкам проверки")
        
        # Кнопка для перехода на страницу статусов и отчётов с иконкой
        self.status_button = ttk.Button(
            button_frame, 
            text="Статус и отчёт 📊", 
            command=self._show_status_page,
            padding="10 5"
        )
        self.status_button.pack(side=tk.LEFT, padx=5)
        create_tooltip(self.status_button, "Перейти к просмотру результатов проверки")
        
        # Создаем разделитель
        ttk.Separator(nav_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5)
        
        # Информация о текущем запуске (справа)
        info_frame = ttk.Frame(nav_frame)
        info_frame.pack(side=tk.RIGHT, padx=10)
        
        ttk.Label(info_frame, text="Текущий номер запуска: ", 
                font=FONT_SMALL_BOLD).pack(side=tk.LEFT)
        
        self.app.run_id_label = ttk.Label(info_frame, text=str(self.app.report_manager.current_run_id), 
                font=FONT_SMALL_BOLD)
        self.app.run_id_label.pack(side=tk.LEFT)
        
        # Добавляем линию-разделитель под навигацией
        separator = ttk.Separator(self.app.root, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, padx=2, pady=0)
        
        # По умолчанию начальная страница - настройки
        self.current_page = "settings"
        self._update_button_state()
        
    def _show_settings_page(self):
        """
        Обработчик нажатия на кнопку настроек
        """
        if self.current_page != "settings":
            # Анимация перехода (мигание кнопки)
            self._button_transition_effect(self.settings_button)
            
            # Показываем страницу настроек
            self.ui_builder.show_settings_page()
            
            # Обновляем состояние и текущую страницу
            self.current_page = "settings"
            self._update_button_state()
    
    def _show_status_page(self):
        """
        Обработчик нажатия на кнопку статуса
        """
        if self.current_page != "status":
            # Анимация перехода (мигание кнопки)
            self._button_transition_effect(self.status_button)
            
            # Показываем страницу статуса
            self.ui_builder.show_status_page()
            
            # Обновляем состояние и текущую страницу
            self.current_page = "status"
            self._update_button_state()
    
    def _update_button_state(self):
        """
        Обновляет состояние кнопок навигации в зависимости от текущей страницы
        """
        if self.current_page == "settings":
            self.settings_button.state(['disabled'])
            self.status_button.state(['!disabled'])
        else:  # status page
            self.settings_button.state(['!disabled'])
            self.status_button.state(['disabled'])
    
    def _button_transition_effect(self, button):
        """
        Создает эффект перехода для кнопки
        """
        # Сохраняем текущее состояние кнопки
        current_state = button.state()
        
        # Делаем кнопку активной на короткое время
        button.state(['active'])
        
        # Восстанавливаем состояние через небольшую задержку
        self.app.root.after(100, lambda: button.state(current_state))
        
    def set_busy_state(self, busy=True):
        """
        Устанавливает состояние занятости (блокирует/разблокирует навигацию)
        
        Параметры:
            busy: True - блокирует навигацию, False - разблокирует
        """
        if busy:
            self.settings_button.state(['disabled'])
            self.status_button.state(['disabled'])
        else:
            self._update_button_state()