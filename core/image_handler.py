from PIL import Image
import os

class ImageHandler:
    """Обработчик изображений подписей"""
    
    @staticmethod
    def load_signature(path):
        """Загрузить изображение подписи"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Файл подписи не найден: {path}")
        
        try:
            img = Image.open(path)
            # Конвертируем в RGBA если нужно
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            return img
        except Exception as e:
            raise Exception(f"Ошибка загрузки изображения: {str(e)}")
    
    @staticmethod
    def resize_signature(img, width, height):
        """Изменить размер подписи"""
        return img.resize((int(width), int(height)), Image.Resampling.LANCZOS)
    
    @staticmethod
    def validate_image(path):
        """Проверить валидность изображения"""
        try:
            with Image.open(path) as img:
                img.verify()
            return True
        except:
            return False
    
    @staticmethod
    def get_image_size(path):
        """Получить размер изображения"""
        with Image.open(path) as img:
            return img.size
    
    @staticmethod
    def save_signature(img, path):
        """Сохранить изображение подписи"""
        img.save(path, 'PNG')