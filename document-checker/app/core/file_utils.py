#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import platform
import subprocess

def normalize_path(path):
    """Заменяет прямые слеши на обратные"""
    return path.replace('/', '\\')

def get_file_type(file_path):
    """Определяет тип файла по расширению"""
    extension = os.path.splitext(file_path)[1].lower()
    
    if extension in ['.docx', '.doc', '.docm']:
        return "Word"
    elif extension in ['.xlsx', '.xls', '.xlsm']:
        return "Excel"
    else:
        return "Неизвестный"

def detect_file_size_category(file_path):
    """
    Определяет категорию размера файла для выбора оптимальной стратегии проверки.
    
    Возвращает:
    - "small": Маленький файл (до 5 МБ)
    - "medium": Средний файл (5-20 МБ)
    - "large": Большой файл (20-100 МБ)
    - "very_large": Очень большой файл (более 100 МБ)
    """
    try:
        file_size = os.path.getsize(file_path)
        # Категории размера (в байтах)
        if file_size < 5 * 1024 * 1024:  # до 5 МБ
            return "small"
        elif file_size < 20 * 1024 * 1024:  # 5-20 МБ
            return "medium"
        elif file_size < 100 * 1024 * 1024:  # 20-100 МБ
            return "large"
        else:  # более 100 МБ
            return "very_large"
    except:
        # По умолчанию считаем файл средним, если невозможно определить размер
        return "medium"

def is_locked_file(file_path):
    """
    Проверяет, не заблокирован ли файл другим процессом.
    """
    try:
        # Пытаемся открыть файл в режиме бинарного чтения+записи
        with open(file_path, "r+b") as f:
            # Файл успешно открыт и не заблокирован
            return False
    except PermissionError:
        # Файл заблокирован другим процессом
        return True
    except:
        # Другие ошибки - считаем, что файл не заблокирован
        return False

def open_file(file_path):
    """Открывает файл с использованием системной программы по умолчанию"""
    try:
        # Проверяем существование файла
        # Для Windows может потребоваться преобразовать пути
        if platform.system() == 'Windows':
            check_path = file_path  # Путь уже в формате с обратными слешами
        else:
            check_path = file_path.replace('\\', '/')  # Для не-Windows систем меняем на прямые слеши
        
        if not os.path.exists(check_path):
            return False, f"Файл не найден:\n{file_path}"
        
        # Нормализуем путь для операционной системы
        system_path = file_path
        if platform.system() != 'Windows':
            # Для не-Windows систем заменяем \ на /
            system_path = file_path.replace('\\', '/')
        
        # Открываем файл соответствующим способом в зависимости от ОС
        if platform.system() == 'Windows':
            os.startfile(system_path)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', system_path))
        else:  # Linux и другие Unix-подобные системы
            subprocess.call(('xdg-open', system_path))
        
        return True, ""
    
    except Exception as e:
        return False, f"Не удалось открыть файл: {str(e)}"

def open_directory(directory_path):
    """Открывает директорию с использованием системной программы по умолчанию"""
    try:
        # Нормализуем путь для операционной системы
        system_path = directory_path
        if platform.system() != 'Windows':
            # Для не-Windows систем заменяем \ на /
            system_path = directory_path.replace('\\', '/')
        
        # Открываем директорию соответствующим способом в зависимости от ОС
        if platform.system() == 'Windows':
            os.startfile(system_path)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', system_path))
        else:  # Linux и другие Unix-подобные системы
            subprocess.call(('xdg-open', system_path))
        
        return True, ""
    
    except Exception as e:
        return False, f"Не удалось открыть директорию: {str(e)}"