#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import concurrent.futures
import threading
from queue import Queue

def init_workers_pool(max_threads=None):
    """
    Создает и возвращает пул рабочих потоков для параллельной обработки
    
    Args:
        max_threads (int, optional): Максимальное количество потоков. 
                                    Если None, будет определено автоматически.
    
    Returns:
        concurrent.futures.ThreadPoolExecutor: Пул потоков для параллельной обработки
    """
    # Определяем оптимальное количество потоков, если не указано явно
    if max_threads is None:
        # Используем не более 75% доступных процессоров или не более 8 потоков
        max_threads = min(8, max(1, int(os.cpu_count() * 0.75)) if os.cpu_count() else 4)
        
    # Создаем и возвращаем пул потоков
    return concurrent.futures.ThreadPoolExecutor(max_workers=max_threads)