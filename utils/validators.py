import os
from config.settings import SUPPORTED_IMAGE_FORMATS, SUPPORTED_PDF_FORMATS

class Validators:
    """Валидаторы для проверки данных"""
    
    @staticmethod
    def validate_person_name(name):
        """Проверить имя человека"""
        if not name or not name.strip():
            return False, "Имя не может быть пустым"
        
        if len(name) > 100:
            return False, "Имя слишком длинное (максимум 100 символов)"
        
        return True, "OK"
    
    @staticmethod
    def validate_signature_file(file_path):
        """Проверить файл подписи"""
        if not os.path.exists(file_path):
            return False, "Файл не существует"
        
        _, ext = os.path.splitext(file_path)
        if ext.lower() not in SUPPORTED_IMAGE_FORMATS:
            return False, f"Неподдерживаемый формат. Используйте: {', '.join(SUPPORTED_IMAGE_FORMATS)}"
        
        return True, "OK"
    
    @staticmethod
    def validate_pdf_file(file_path):
        """Проверить PDF файл"""
        if not os.path.exists(file_path):
            return False, "Файл не существует"
        
        _, ext = os.path.splitext(file_path)
        if ext.lower() not in SUPPORTED_PDF_FORMATS:
            return False, "Файл должен быть в формате PDF"
        
        return True, "OK"
    
    @staticmethod
    def validate_position(x, y, width, height, page_width, page_height):
        """Проверить позицию подписи"""
        if x < 0 or y < 0:
            return False, "Координаты не могут быть отрицательными"
        
        if width <= 0 or height <= 0:
            return False, "Размеры должны быть положительными"
        
        if x + width > page_width:
            return False, "Подпись выходит за пределы страницы по ширине"
        
        if y + height > page_height:
            return False, "Подпись выходит за пределы страницы по высоте"
        
        return True, "OK"