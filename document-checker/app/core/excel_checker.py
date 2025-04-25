#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import openpyxl
from zipfile import ZipFile
import win32com.client
import pythoncom

def check_excel_file(file_path, file_name):
    """Проверка Excel файла с оптимизацией для крупных файлов"""
    try:
        issues = []
        
        if file_path.lower().endswith(('.xlsx', '.xlsm')):
            # Быстрая предварительная проверка для .xlsx и .xlsm без полной загрузки
            try:
                from zipfile import ZipFile
                with ZipFile(file_path) as xlsx_zip:
                    # Проверка на комментарии - смотрим наличие файлов комментариев
                    comment_files = [f for f in xlsx_zip.namelist() if 'comments' in f.lower()]
                    if comment_files:
                        issues.append("комментарии")
                    
                    # Проверка цвета вкладок - загружаем workbook.xml
                    if 'xl/workbook.xml' in xlsx_zip.namelist():
                        workbook_content = xlsx_zip.read('xl/workbook.xml').decode('utf-8', errors='ignore')
                        if 'tabColor' in workbook_content:
                            # Более тщательная проверка на цвета листов
                            if any(color in workbook_content for color in ['FFFF', 'FF0000', 'FFFF00', 'FFF000']):
                                issues.append("цветной лист")
            except Exception as e:
                # В случае ошибки быстрой проверки, продолжаем обычным способом
                pass
                
            # Если проблем с цветами листов не найдено быстрым способом, выполняем более тщательную проверку
            if not "цветной лист" in issues:
                # Используем openpyxl с оптимизированной загрузкой
                options = {
                    'read_only': False,  # Нужно отключить read_only для доступа к цветам
                    'data_only': True    # Без формул
                }
                
                wb = None
                try:
                    wb = openpyxl.load_workbook(file_path, **options)
                    
                    # Проверка на желтые или красные листы
                    for sheet_name in wb.sheetnames:
                        try:
                            sheet = wb[sheet_name]
                            if sheet.sheet_properties and sheet.sheet_properties.tabColor:
                                tab_color = sheet.sheet_properties.tabColor.rgb
                                # Более широкая проверка на различные оттенки желтого и красного
                                if tab_color:
                                    # Различные варианты цветов
                                    yellow_codes = ['FFFF00', 'FFFFF00', 'FFFFFF00', 'FFF0F000', 'FFFFCC']
                                    red_codes = ['FF0000', 'FFFF0000', 'FFF00000', 'FFCC0000']
                                    
                                    # Проверка на желтый/красный цвет
                                    is_yellow = any(code in tab_color.upper() for code in yellow_codes)
                                    is_red = any(code in tab_color.upper() for code in red_codes)
                                    
                                    if is_yellow or is_red:
                                        issues.append(f"цветной лист ({sheet_name})")
                                        break
                        except Exception as e:
                            # Логируем ошибку и продолжаем
                            continue
                    
                    # Если всё еще не найдены цветные листы, проверяем альтернативным способом
                    if not "цветной лист" in issues:
                        for sheet_name in wb.sheetnames:
                            try:
                                sheet = wb[sheet_name]
                                # Дополнительная проверка через свойства листа
                                if hasattr(sheet, '_WorkbookChild__props') and 'tabColor' in sheet._WorkbookChild__props:
                                    issues.append(f"цветной лист ({sheet_name})")
                                    break
                            except:
                                pass
                
                    # Проверка на желтые ячейки - только для первых 1000 ячеек каждого листа
                    if not "желтые ячейки" in issues:
                        for sheet_name in wb.sheetnames:
                            try:
                                sheet = wb[sheet_name]
                                cell_count = 0
                                max_cells = 1000  # Ограничиваем количество проверяемых ячеек
                                
                                for row in sheet.iter_rows():
                                    for cell in row:
                                        cell_count += 1
                                        if cell_count > max_cells:
                                            break
                                            
                                        if cell.fill and hasattr(cell.fill, 'start_color') and hasattr(cell.fill.start_color, 'index'):
                                            fill_color = cell.fill.start_color.index
                                            if isinstance(fill_color, str) and ('FFFF' in fill_color or 'FFFF00' in fill_color or 'FFF0' in fill_color):
                                                issues.append("желтые ячейки")
                                                break
                                    if cell_count > max_cells or "желтые ячейки" in issues:
                                        break
                                if "желтые ячейки" in issues:
                                    break
                            except Exception:
                                # Если возникла ошибка при проверке листа, продолжаем с следующим
                                continue
                    
                    # Проверка на комментарии - только если еще не найдены
                    if not "комментарии" in issues:
                        for sheet_name in wb.sheetnames:
                            try:
                                sheet = wb[sheet_name]
                                cell_count = 0
                                max_cells = 1000  # Ограничиваем количество проверяемых ячеек
                                
                                for row in sheet.iter_rows():
                                    for cell in row:
                                        cell_count += 1
                                        if cell_count > max_cells:
                                            break
                                            
                                        if cell.comment is not None:
                                            issues.append("комментарии")
                                            break
                                    if cell_count > max_cells or "комментарии" in issues:
                                        break
                                if "комментарии" in issues:
                                    break
                            except Exception:
                                continue
                finally:
                    # Закрываем только если wb было инициализировано
                    if wb is not None:
                        wb.close()
        else:
            # Используем win32com для .xls с ограничениями
            pythoncom.CoInitialize()
            excel_app = None
            try:
                excel_app = win32com.client.Dispatch("Excel.Application")
                excel_app.Visible = False
                excel_app.DisplayAlerts = False
                excel_app.ScreenUpdating = False  # Выключаем обновление экрана для ускорения
                
                wb = None
                try:
                    wb = excel_app.Workbooks.Open(file_path, ReadOnly=True, UpdateLinks=False)
                    
                    # Проверка только первых нескольких листов
                    max_sheets = min(3, wb.Sheets.Count)
                    
                    for i in range(1, max_sheets + 1):
                        sheet = wb.Sheets(i)
                        
                        # Проверка на цвет листа
                        try:
                            if sheet.Tab.ColorIndex in [6, 3, 36, 44, 46]:  # Расширенный список: 6-желтый, 3-красный и другие оттенки
                                issues.append(f"цветной лист ({sheet.Name})")
                                break
                        except:
                            pass
                        
                        # Если цвет не определился по ColorIndex, пробуем альтернативный метод через RGB
                        if not "цветной лист" in issues:
                            try:
                                tab_color = sheet.Tab.Color
                                if tab_color:
                                    # Преобразуем в RGB для проверки
                                    r = tab_color % 256
                                    g = (tab_color // 256) % 256
                                    b = (tab_color // 65536) % 256
                                    
                                    # Проверка на желтый (высокие значения R и G, низкое B)
                                    if (r > 200 and g > 200 and b < 100) or (r > 200 and g < 100 and b < 100):
                                        issues.append(f"цветной лист ({sheet.Name})")
                                        break
                            except:
                                pass
                        
                        # Проверка на желтые ячейки - только для ограниченного диапазона
                        if not "желтые ячейки" in issues:
                            try:
                                used_range = sheet.UsedRange
                                if used_range:
                                    # Определяем размеры используемого диапазона
                                    rows_count = min(100, used_range.Rows.Count)  # Проверяем максимум 100 строк
                                    cols_count = min(20, used_range.Columns.Count)  # Проверяем максимум 20 столбцов
                                    
                                    for row in range(1, rows_count + 1):
                                        for col in range(1, cols_count + 1):
                                            try:
                                                cell = sheet.Cells(row, col)
                                                if cell and cell.Interior and cell.Interior.ColorIndex == 6:  # 6 - желтый в Excel
                                                    issues.append("желтые ячейки")
                                                    break
                                            except:
                                                pass
                                        if "желтые ячейки" in issues:
                                            break
                            except:
                                pass
                        
                        # Проверка на комментарии
                        if not "комментарии" in issues:
                            try:
                                if sheet.Comments and sheet.Comments.Count > 0:
                                    issues.append("комментарии")
                            except:
                                pass
                        
                        # Если все проблемы уже найдены, прекращаем проверку
                        if "комментарии" in issues and "желтые ячейки" in issues and "цветной лист" in issues:
                            break
                finally:
                    # Закрываем только если wb было инициализировано
                    if wb is not None:
                        wb.Close(False)
            finally:
                # Выходим из Excel только если приложение было запущено
                if excel_app is not None:
                    excel_app.Quit()
        
        # Формирование результата
        if issues:
            result = "Не пройден"
            comment = "Найдено: " + ", ".join(set(issues))
        else:
            result = "Пройден"
            comment = "Проблем не обнаружено"
        
        return {
            'file_name': file_name,
            'file_type': "Excel",
            'file_path': file_path,
            'result': result,
            'comment': comment
        }
        
    except Exception as e:
        return {
            'file_name': file_name,
            'file_type': "Excel",
            'file_path': file_path,
            'result': "Ошибка",
            'comment': f"Ошибка проверки: {str(e)}"
        }