#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Вспомогательные методы для работы с интерфейсом
"""
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import sys
import platform
import subprocess

class UIUtils:
    """
    Вспомогательные методы для работы с интерфейсом
    """
    @staticmethod
    def center_window(window, width=800, height=600):
        """
        Центрирует окно на экране и устанавливает минимальный размер
        """
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Устанавливаем минимальные размеры окна
        window.minsize(width=640, height=480)
    
    @staticmethod
    def truncate_path(path, max_length=40):
        """
        Сокращает длинный путь, заменяя среднюю часть многоточием
        
        Параметры:
            path: Путь к файлу или папке
            max_length: Максимальная длина отображаемого пути
            
        Возвращает:
            Сокращенный путь
        """
        if not path or len(path) <= max_length:
            return path
            
        # Получаем разделитель путей в зависимости от ОС
        sep = os.path.sep
        
        # Разбиваем путь на части
        parts = path.split(sep)
        
        # Если путь состоит всего из 2-3 частей, просто возвращаем его
        if len(parts) <= 3:
            return path
            
        # Оставляем первую и последнюю часть
        first_part = parts[0]
        last_part = sep.join(parts[-2:])  # Последние две части
        
        # Формируем сокращенный путь
        truncated = f"{first_part}{sep}...{sep}{last_part}"
        
        # Если еще слишком длинный, сокращаем еще больше
        if len(truncated) > max_length and len(parts) > 3:
            last_part = parts[-1]  # Только последняя часть
            truncated = f"{first_part}{sep}...{sep}{last_part}"
            
        return truncated
    
    @staticmethod
    def open_file(file_path):
        """
        Открывает файл в ассоциированной программе
        
        Параметры:
            file_path: Путь к файлу
            
        Возвращает:
            True, если файл успешно открыт, иначе False
        """
        try:
            if platform.system() == 'Windows':
                os.startfile(file_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', file_path))
            else:  # Linux и другие Unix-подобные ОС
                subprocess.call(('xdg-open', file_path))
            return True
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть файл: {str(e)}")
            return False
    
    @staticmethod
    def open_directory(dir_path):
        """
        Открывает директорию в файловом менеджере
        
        Параметры:
            dir_path: Путь к директории или к файлу, чью директорию нужно открыть
            
        Возвращает:
            True, если директория успешно открыта, иначе False
        """
        try:
            # Если передан путь к файлу, получаем директорию
            if os.path.isfile(dir_path):
                dir_path = os.path.dirname(dir_path)
                
            if platform.system() == 'Windows':
                os.startfile(dir_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', dir_path))
            else:  # Linux и другие Unix-подобные ОС
                subprocess.call(('xdg-open', dir_path))
            return True
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть директорию: {str(e)}")
            return False
    
    @staticmethod
    def copy_to_clipboard(root, text):
        """
        Копирует текст в буфер обмена
        
        Параметры:
            root: Корневой виджет (обычно окно Tk)
            text: Текст для копирования
            
        Возвращает:
            True, если текст успешно скопирован, иначе False
        """
        try:
            root.clipboard_clear()
            root.clipboard_append(text)
            return True
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось скопировать текст: {str(e)}")
            return False
    
    @staticmethod
    def ask_confirm(title, message):
        """
        Показывает диалог подтверждения действия
        
        Параметры:
            title: Заголовок диалогового окна
            message: Текст сообщения
            
        Возвращает:
            True, если пользователь подтвердил действие, иначе False
        """
        return messagebox.askyesno(title, message)
    
    @staticmethod
    def browse_folder(initial_dir=None):
        """
        Открывает диалог выбора папки
        
        Параметры:
            initial_dir: Начальная директория для диалога
            
        Возвращает:
            Выбранный путь или None, если диалог был отменен
        """
        folder_path = filedialog.askdirectory(
            title="Выберите папку",
            initialdir=initial_dir or os.path.expanduser("~")
        )
        return folder_path if folder_path else None
    
    @staticmethod
    def browse_file(filetypes=None, initial_dir=None):
        """
        Открывает диалог выбора файла
        
        Параметры:
            filetypes: Список кортежей с типами файлов (описание, маска)
            initial_dir: Начальная директория для диалога
            
        Возвращает:
            Выбранный путь или None, если диалог был отменен
        """
        if filetypes is None:
            filetypes = [
                ("Все файлы", "*.*"),
                ("Документы Word", "*.doc;*.docx;*.docm"),
                ("Таблицы Excel", "*.xls;*.xlsx;*.xlsm")
            ]
            
        file_path = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=filetypes,
            initialdir=initial_dir or os.path.expanduser("~")
        )
        return file_path if file_path else None
    
    @staticmethod
    def browse_save_file(defaultextension=".xlsx", filetypes=None, initial_dir=None, initial_file=None):
        """
        Открывает диалог сохранения файла
        
        Параметры:
            defaultextension: Расширение по умолчанию
            filetypes: Список кортежей с типами файлов (описание, маска)
            initial_dir: Начальная директория для диалога
            initial_file: Имя файла по умолчанию
            
        Возвращает:
            Выбранный путь или None, если диалог был отменен
        """
        if filetypes is None:
            filetypes = [
                ("Excel файлы", "*.xlsx"),
                ("Все файлы", "*.*")
            ]
            
        file_path = filedialog.asksaveasfilename(
            title="Сохранить отчет как",
            defaultextension=defaultextension,
            filetypes=filetypes,
            initialdir=initial_dir or os.path.expanduser("~"),
            initialfile=initial_file or "отчет.xlsx"
        )
        return file_path if file_path else None