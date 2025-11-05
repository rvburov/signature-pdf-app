import os
import shutil
from config.settings import SIGNATURES_DIR

class FileUtils:
    """Утилиты для работы с файлами"""
    
    @staticmethod
    def copy_signature_file(source_path, person_name):
        """
        Копировать файл подписи в папку программы
        
        Args:
            source_path: путь к исходному файлу
            person_name: имя человека для формирования имени файла
        
        Returns:
            Путь к скопированному файлу
        """
        # Получаем расширение файла
        _, ext = os.path.splitext(source_path)
        
        # Формируем безопасное имя файла
        safe_name = person_name.replace(' ', '_').replace('/', '_').replace('\\', '_')
        new_filename = f"{safe_name}{ext}"
        new_path = os.path.join(SIGNATURES_DIR, new_filename)
        
        # Если файл с таким именем уже существует, добавляем номер
        counter = 1
        while os.path.exists(new_path):
            new_filename = f"{safe_name}_{counter}{ext}"
            new_path = os.path.join(SIGNATURES_DIR, new_filename)
            counter += 1
        
        # Копируем файл
        shutil.copy2(source_path, new_path)
        
        return new_path
    
    @staticmethod
    def delete_signature_file(file_path):
        """Удалить файл подписи"""
        if os.path.exists(file_path):
            os.remove(file_path)
    
    @staticmethod
    def get_file_size(file_path):
        """Получить размер файла в байтах"""
        return os.path.getsize(file_path)
    
    @staticmethod
    def format_file_size(size_bytes):
        """Форматировать размер файла в читаемый вид"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    @staticmethod
    def ensure_dir_exists(directory):
        """Убедиться что директория существует"""
        os.makedirs(directory, exist_ok=True)