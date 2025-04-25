#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import tkinter as tk
from tkinter import ttk

# Импортируем только основной класс приложения
from app.document_checker import DocumentChecker

def main():
    root = tk.Tk()
    
    # Установка иконки приложения (если доступна)
    try:
        if getattr(sys, 'frozen', False):
            # В скомпилированной версии
            app_path = os.path.dirname(sys.executable)
            icon_path = os.path.join(app_path, "resources", "app_icon.ico")
        else:
            # В режиме скрипта
            app_path = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(app_path, "resources", "app_icon.ico")
            
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
    except Exception:
        # Если не удалось установить иконку, продолжаем без неё
        pass
    
    # Устанавливаем тему и стиль
    try:
        style = ttk.Style()
        # Пытаемся использовать современную тему, если доступна
        available_themes = style.theme_names()
        if 'vista' in available_themes:
            style.theme_use('vista')
        elif 'winnative' in available_themes:
            style.theme_use('winnative')
        elif 'clam' in available_themes:
            style.theme_use('clam')
    except Exception:
        # Если не удалось установить тему, используем тему по умолчанию
        pass
    
    # Создаем экземпляр приложения
    app = DocumentChecker(root)
    
    # Инициализация контекстного меню
    app.setup_context_menu()
    
    # Проверяем аргументы командной строки
    if len(sys.argv) > 1:
        # Если приложение запущено с путем в аргументах
        path_arg = sys.argv[1]
        if os.path.exists(path_arg):
            app.selected_path.set(path_arg)
    
    # Центрируем окно на экране
    window_width = 1000
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_pos = (screen_width - window_width) // 2
    y_pos = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
    
    # Запускаем главный цикл обработки событий
    root.mainloop()

if __name__ == "__main__":
    main()