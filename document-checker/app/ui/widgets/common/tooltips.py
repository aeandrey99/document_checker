#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль для создания и управления всплывающими подсказками
"""

import tkinter as tk
from ...theme import TEXT_PRIMARY, SURFACE, FONT_SMALL

class ToolTip:
    """
    Класс для создания всплывающих подсказок для виджетов
    """
    def __init__(self, widget, text='', delay=500, wrap_length=250):
        """
        Инициализирует подсказку для виджета
        
        Параметры:
            widget: Виджет, к которому привязывается подсказка
            text: Текст подсказки
            delay: Задержка перед показом подсказки в миллисекундах
            wrap_length: Длина строки, после которой текст переносится
        """
        self.widget = widget
        self.text = text
        self.delay = delay
        self.wrap_length = wrap_length
        self.tooltip_window = None
        self.id = None
        
        # Привязываем события
        self.widget.bind("<Enter>", self.on_enter, add="+")
        self.widget.bind("<Leave>", self.on_leave, add="+")
        self.widget.bind("<ButtonPress>", self.on_leave, add="+")

    def on_enter(self, event=None):
        """Запускает таймер показа подсказки при наведении на виджет"""
        self.schedule()

    def on_leave(self, event=None):
        """Скрывает подсказку при уходе с виджета"""
        self.unschedule()
        self.hide_tooltip()

    def schedule(self):
        """Планирует отображение подсказки"""
        self.unschedule()
        self.id = self.widget.after(self.delay, self.show_tooltip)

    def unschedule(self):
        """Отменяет запланированное отображение подсказки"""
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None

    def show_tooltip(self):
        """Отображает окно подсказки"""
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        # Создаем окно подсказки
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)  # Убираем рамку окна
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        # Создаем метку с текстом
        label = tk.Label(
            self.tooltip_window,
            text=self.text,
            background=SURFACE,
            foreground=TEXT_PRIMARY,
            relief="solid",
            borderwidth=1,
            font=FONT_SMALL,
            wraplength=self.wrap_length,
            justify="left",
            padx=5,
            pady=3
        )
        label.pack()

    def hide_tooltip(self):
        """Скрывает окно подсказки"""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

def create_tooltip(widget, text, delay=500, wrap_length=250):
    """
    Создает подсказку для виджета
    
    Параметры:
        widget: Виджет, к которому привязывается подсказка
        text: Текст подсказки
        delay: Задержка перед показом подсказки в миллисекундах
        wrap_length: Длина строки, после которой текст переносится
    
    Возвращает:
        Объект ToolTip
    """
    return ToolTip(widget, text, delay, wrap_length)