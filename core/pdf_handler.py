from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from PIL import Image
import os

class PDFHandler:
    """Обработчик PDF файлов"""
    
    @staticmethod
    def get_page_count(pdf_path):
        """Получить количество страниц в PDF"""
        reader = PdfReader(pdf_path)
        return len(reader.pages)
    
    @staticmethod
    def get_page_size(pdf_path, page_num=0):
        """Получить размер страницы PDF"""
        reader = PdfReader(pdf_path)
        page = reader.pages[page_num]
        box = page.mediabox
        return float(box.width), float(box.height)
    
    @staticmethod
    def validate_pdf(path):
        """Проверить валидность PDF файла"""
        try:
            reader = PdfReader(path)
            return len(reader.pages) > 0
        except:
            return False
    
    @staticmethod
    def create_signature_overlay(signature_img, x, y, width, height, page_width, page_height):
        """Создать overlay с подписью"""
        # Создаем буфер для PDF
        packet = BytesIO()
        
        # Создаем canvas
        c = canvas.Canvas(packet, pagesize=(page_width, page_height))
        
        # Сохраняем изображение во временный буфер
        img_buffer = BytesIO()
        signature_img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        # Рисуем изображение на canvas
        # В PDF координаты идут снизу вверх, поэтому инвертируем Y
        y_inverted = page_height - y - height
        c.drawImage(img_buffer, x, y_inverted, width=width, height=height, mask='auto')
        
        c.save()
        
        # Возвращаем в начало буфера
        packet.seek(0)
        
        return packet
    
    @staticmethod
    def add_signature_to_pdf(input_path, output_path, signature_img, position):
        """Добавить подпись в PDF"""
        # Читаем исходный PDF
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        # Получаем размер страницы
        page = reader.pages[position.page]
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)
        
        # Создаем overlay с подписью
        overlay_packet = PDFHandler.create_signature_overlay(
            signature_img,
            position.x,
            position.y,
            position.width,
            position.height,
            page_width,
            page_height
        )
        
        # Читаем overlay
        overlay_reader = PdfReader(overlay_packet)
        overlay_page = overlay_reader.pages[0]
        
        # Проходим по всем страницам
        for i, page in enumerate(reader.pages):
            if i == position.page:
                # На нужной странице накладываем подпись
                page.merge_page(overlay_page)
            writer.add_page(page)
        
        # Сохраняем результат
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
    
    @staticmethod
    def pdf_to_image(pdf_path, page_num=0, dpi=150):
        """Конвертировать страницу PDF в изображение для предварительного просмотра"""
        try:
            from pdf2image import convert_from_path
            images = convert_from_path(pdf_path, dpi=dpi, first_page=page_num+1, last_page=page_num+1)
            if images:
                return images[0]
        except ImportError:
            # Если pdf2image не установлен, возвращаем заглушку
            pass
        return None