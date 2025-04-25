# Утилиты для многопоточности
import threading

def run_in_thread(target, args=()):
    thread = threading.Thread(target=target, args=args)
    thread.start()
    return thread
