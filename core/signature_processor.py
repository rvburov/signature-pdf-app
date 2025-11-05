import os
from core.pdf_handler import PDFHandler
from core.image_handler import ImageHandler
from config.settings import OUTPUT_DIR

class SignatureProcessor:
    """Процессор для обработки подписей и создания документов"""
    
    def __init__(self):
        self.pdf_handler = PDFHandler()
        self.image_handler = ImageHandler()
    
    def process_single(self, pdf_path, person, position, output_filename=None):
        """
        Обработать один документ для одного человека
        
        Args:
            pdf_path: путь к PDF шаблону
            person: объект Person с данными человека
            position: объект SignaturePosition с позицией подписи
            output_filename: имя выходного файла (опционально)
        
        Returns:
            Путь к созданному файлу
        """
        # Загружаем изображение подписи
        signature_img = self.image_handler.load_signature(person.signature_path)
        
        # Изменяем размер подписи
        signature_img = self.image_handler.resize_signature(
            signature_img,
            position.width,
            position.height
        )
        
        # Формируем имя выходного файла
        if output_filename is None:
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            output_filename = f"{base_name}_{person.name.replace(' ', '_')}.pdf"
        
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        # Добавляем подпись в PDF
        self.pdf_handler.add_signature_to_pdf(
            pdf_path,
            output_path,
            signature_img,
            position
        )
        
        return output_path
    
    def process_batch(self, pdf_path, persons, position, progress_callback=None):
        """
        Обработать документ для нескольких людей
        
        Args:
            pdf_path: путь к PDF шаблону
            persons: список объектов Person
            position: объект SignaturePosition с позицией подписи
            progress_callback: функция обратного вызова для отслеживания прогресса
        
        Returns:
            Список путей к созданным файлам
        """
        output_files = []
        total = len(persons)
        
        for i, person in enumerate(persons):
            try:
                output_path = self.process_single(pdf_path, person, position)
                output_files.append(output_path)
                
                if progress_callback:
                    progress_callback(i + 1, total, person.name)
            except Exception as e:
                print(f"Ошибка обработки для {person.name}: {str(e)}")
                if progress_callback:
                    progress_callback(i + 1, total, f"Ошибка: {person.name}")
        
        return output_files
    
    def validate_inputs(self, pdf_path, person, position):
        """
        Проверить валидность входных данных
        
        Returns:
            (bool, str): (валидность, сообщение об ошибке)
        """
        # Проверка PDF
        if not os.path.exists(pdf_path):
            return False, "PDF файл не найден"
        
        if not self.pdf_handler.validate_pdf(pdf_path):
            return False, "Невалидный PDF файл"
        
        # Проверка подписи
        if not os.path.exists(person.signature_path):
            return False, f"Файл подписи не найден: {person.signature_path}"
        
        if not self.image_handler.validate_image(person.signature_path):
            return False, "Невалидное изображение подписи"
        
        # Проверка позиции
        page_count = self.pdf_handler.get_page_count(pdf_path)
        if position.page >= page_count:
            return False, f"Страница {position.page} не существует в документе"
        
        return True, "OK"