# build_script.py с дополнительными файлами
import PyInstaller.__main__

PyInstaller.__main__.run([
    'C:\Users\kills\Downloads\Макросы\Программа по отчету о файлах\document-checker\main.py',
    '--onefile',
    '--noconsole',
    '--name=Проверка документов 1.6',
    '--add-data=assets;assets',  # Пример добавления папки assets
    '--distpath=dist',
    '--workpath=build',
    '--specpath=spec'
])