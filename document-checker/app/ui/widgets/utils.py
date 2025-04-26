#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class UIUtils:
    """
    Вспомогательные методы для работы с интерфейсом
    """
    @staticmethod
    def center_window(window, width=800, height=600):
        """
        Центрирует окно на экране
        """
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        window.geometry(f"{width}x{height}+{x}+{y}")
        
    @staticmethod
    def create_styles():
        """
        Создает стили для элементов интерфейса
        """
        style = ttk.Style()
        
        # Настройка цветов и шрифтов
        style.configure("TButton", font=("", 9))
        style.configure("TLabel", font=("", 9))
        style.configure("TCheckbutton", font=("", 9))
        
        # Особые стили для заголовков
        style.configure("Title.TLabel", font=("", 10, "bold"))
        
        return style