#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import json

class ConfigManager:
    """
    Класс для управления настройками приложения.
    """
    def __init__(self, app_instance):
        self.app = app_instance
        
        # Определяем путь для сохранения/загрузки настроек
        if getattr(sys, 'frozen', False):
            self.app_dir = os.path.dirname(sys.executable)
        else:
            self.app_dir = os.path.dirname(os.path.abspath(__file__))
            # Перемещаемся на два уровня вверх (utils -> app -> document-checker)
            self.app_dir = os.path.dirname(os.path.dirname(self.app_dir))
        
        self.settings_path = os.path.join(self.app_dir, "document_checker_settings.json")
    
    def save_settings(self):
        """
        Сохраняет настройки приложения в файл JSON.
        """
        try:
            settings = {
                "check_docx": self.app.check_docx.get(),
                "check_doc": self.app.check_doc.get(),
                "check_docm": self.app.check_docm.get(),
                "check_xlsx": self.app.check_xlsx.get(),
                "check_xls": self.app.check_xls.get(),
                "check_xlsm": self.app.check_xlsm.get(),
                "output_path": self.app.output_path.get(),
                "last_selected_path": self.app.selected_path.get(),
                "enable_value_search": self.app.enable_value_search.get(),
                "search_values": self.app.search_values.get(),
                "max_threads": self.app.max_threads.get(),
                "skip_large_files": self.app.skip_large_files.get()
            }
            
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=4)
            return True
                
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")
            return False
    
    def load_settings(self):
        """
        Загружает настройки приложения из файла JSON.
        """
        try:
            # Проверяем существование файла настроек
            if not os.path.exists(self.settings_path):
                return False
            
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                
            # Применяем загруженные настройки
            if "check_docx" in settings:
                self.app.check_docx.set(settings["check_docx"])
            if "check_doc" in settings:
                self.app.check_doc.set(settings["check_doc"])
            if "check_docm" in settings:
                self.app.check_docm.set(settings["check_docm"])
            if "check_xlsx" in settings:
                self.app.check_xlsx.set(settings["check_xlsx"])
            if "check_xls" in settings:
                self.app.check_xls.set(settings["check_xls"])
            if "check_xlsm" in settings:
                self.app.check_xlsm.set(settings["check_xlsm"])
            if "output_path" in settings:
                self.app.output_path.set(settings["output_path"])
            if "last_selected_path" in settings:
                self.app.selected_path.set(settings["last_selected_path"])
            if "max_threads" in settings:
                self.app.max_threads.set(settings["max_threads"])
            if "skip_large_files" in settings:
                self.app.skip_large_files.set(settings["skip_large_files"])
            
            # Загружаем настройки поиска значений
            if "enable_value_search" in settings:
                self.app.enable_value_search.set(settings["enable_value_search"])
            if "search_values" in settings:
                self.app.search_values.set(settings["search_values"])
            
            return True
                
        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}")
            return False
    
    def get_default_output_path(self):
        """
        Возвращает путь для сохранения отчета по умолчанию.
        """
        return os.path.join(self.app_dir, "Отчет_проверки_документов.xlsx")