from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from config.settings import PREVIEW_MAX_WIDTH, PREVIEW_MAX_HEIGHT

class PreviewWidget(QWidget):
    """Виджет предварительного просмотра PDF с позицией подписи"""
    
    def __init__(self):
        super().__init__()
        self.pdf_path = None
        self.position = None
        self.pdf_pixmap = None
        
        self.init_ui()
    
    def init_ui(self):
        """Инициализация интерфейса"""
        layout = QVBoxLayout(self)
        
        # Заголовок
        title = QLabel("Предварительный просмотр")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Область прокрутки
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        # Label для отображения PDF
        self.preview_label = PreviewLabel()
        scroll.setWidget(self.preview_label)
        
        layout.addWidget(scroll)
    
    def load_pdf(self, pdf_path):
        """Загрузить PDF для предварительного просмотра"""
        self.pdf_path = pdf_path
        
        try:
            # Пытаемся конвертировать первую страницу в изображение
            from core.pdf_handler import PDFHandler
            img = PDFHandler.pdf_to_image(pdf_path, page_num=0, dpi=100)
            
            if img:
                # Конвертируем PIL Image в QPixmap
                img_rgb = img.convert('RGB')
                img_rgb.save('/tmp/preview.png')
                self.pdf_pixmap = QPixmap('/tmp/preview.png')
            else:
                # Заглушка если pdf2image не установлен
                self.pdf_pixmap = self.create_placeholder()
        
        except Exception as e:
            print(f"Ошибка загрузки PDF для просмотра: {e}")
            self.pdf_pixmap = self.create_placeholder()
        
        self.update_preview()
    
    def create_placeholder(self):
        """Создать заглушку для предварительного просмотра"""
        pixmap = QPixmap(600, 800)
        pixmap.fill(QColor(240, 240, 240))
        
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        painter.drawRect(10, 10, 580, 780)
        painter.drawText(pixmap.rect(), Qt.AlignCenter, 
                        "Предварительный просмотр\n(установите pdf2image для полного просмотра)")
        painter.end()
        
        return pixmap
    
    def update_signature_position(self, position):
        """Обновить позицию подписи"""
        self.position = position
        self.update_preview()
    
    def update_preview(self):
        """Обновить предварительный просмотр"""
        if not self.pdf_pixmap:
            return
        
        # Копируем оригинальный pixmap
        display_pixmap = self.pdf_pixmap.copy()
        
        # Если есть позиция, рисуем прямоугольник
        if self.position:
            painter = QPainter(display_pixmap)
            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.drawRect(
                int(self.position.x),
                int(self.position.y),
                int(self.position.width),
                int(self.position.height)
            )
            painter.end()
        
        # Масштабируем если нужно
        if display_pixmap.width() > PREVIEW_MAX_WIDTH or display_pixmap.height() > PREVIEW_MAX_HEIGHT:
            display_pixmap = display_pixmap.scaled(
                PREVIEW_MAX_WIDTH,
                PREVIEW_MAX_HEIGHT,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        
        self.preview_label.setPixmap(display_pixmap)


class PreviewLabel(QLabel):
    """Расширенный Label для предварительного просмотра"""
    
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setText("Загрузите PDF файл")
        self.setMinimumSize(400, 500)
        self.setStyleSheet("background-color: white; border: 1px solid #ccc;")