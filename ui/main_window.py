from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFileDialog, QMessageBox, QGroupBox,
                             QSpinBox, QDoubleSpinBox, QComboBox, QStatusBar)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from config.settings import WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
from ui.signature_manager import SignatureManagerDialog
from ui.preview_widget import PreviewWidget
from ui.batch_processor import BatchProcessorDialog
from database.db_manager import DatabaseManager
from database.models import SignaturePosition
from core.signature_processor import SignatureProcessor
import os

class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.signature_processor = SignatureProcessor()
        self.current_pdf_path = None
        self.current_position = SignaturePosition()
        
        self.init_ui()
    
    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle("PDF Signature Tool")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QHBoxLayout(central_widget)
        
        # Левая панель (управление)
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)
        
        # Правая панель (предварительный просмотр)
        self.preview_widget = PreviewWidget()
        main_layout.addWidget(self.preview_widget, 2)
        
        # Статус бар
        self.statusBar().showMessage("Готов к работе")
    
    def create_left_panel(self):
        """Создать левую панель управления"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Загрузка PDF
        pdf_group = QGroupBox("1. PDF Шаблон")
        pdf_layout = QVBoxLayout()
        
        self.pdf_label = QLabel("Файл не загружен")
        self.pdf_label.setWordWrap(True)
        pdf_layout.addWidget(self.pdf_label)
        
        load_pdf_btn = QPushButton("Загрузить PDF")
        load_pdf_btn.clicked.connect(self.load_pdf)
        pdf_layout.addWidget(load_pdf_btn)
        
        pdf_group.setLayout(pdf_layout)
        layout.addWidget(pdf_group)
        
        # Позиция подписи
        position_group = QGroupBox("2. Позиция подписи")
        position_layout = QVBoxLayout()
        
        # Номер страницы
        page_layout = QHBoxLayout()
        page_layout.addWidget(QLabel("Страница:"))
        self.page_spin = QSpinBox()
        self.page_spin.setMinimum(0)
        self.page_spin.valueChanged.connect(self.on_position_changed)
        page_layout.addWidget(self.page_spin)
        position_layout.addLayout(page_layout)
        
        # X координата
        x_layout = QHBoxLayout()
        x_layout.addWidget(QLabel("X:"))
        self.x_spin = QDoubleSpinBox()
        self.x_spin.setMaximum(10000)
        self.x_spin.valueChanged.connect(self.on_position_changed)
        x_layout.addWidget(self.x_spin)
        position_layout.addLayout(x_layout)
        
        # Y координата
        y_layout = QHBoxLayout()
        y_layout.addWidget(QLabel("Y:"))
        self.y_spin = QDoubleSpinBox()
        self.y_spin.setMaximum(10000)
        self.y_spin.valueChanged.connect(self.on_position_changed)
        y_layout.addWidget(self.y_spin)
        position_layout.addLayout(y_layout)
        
        # Ширина
        width_layout = QHBoxLayout()
        width_layout.addWidget(QLabel("Ширина:"))
        self.width_spin = QDoubleSpinBox()
        self.width_spin.setMaximum(1000)
        self.width_spin.setValue(150)
        self.width_spin.valueChanged.connect(self.on_position_changed)
        width_layout.addWidget(self.width_spin)
        position_layout.addLayout(width_layout)
        
        # Высота
        height_layout = QHBoxLayout()
        height_layout.addWidget(QLabel("Высота:"))
        self.height_spin = QDoubleSpinBox()
        self.height_spin.setMaximum(1000)
        self.height_spin.setValue(50)
        self.height_spin.valueChanged.connect(self.on_position_changed)
        height_layout.addWidget(self.height_spin)
        position_layout.addLayout(height_layout)
        
        position_group.setLayout(position_layout)
        layout.addWidget(position_group)
        
        # Управление подписями
        signatures_group = QGroupBox("3. Подписи")
        signatures_layout = QVBoxLayout()
        
        manage_btn = QPushButton("Управление подписями")
        manage_btn.clicked.connect(self.open_signature_manager)
        signatures_layout.addWidget(manage_btn)
        
        signatures_group.setLayout(signatures_layout)
        layout.addWidget(signatures_group)
        
        # Обработка
        process_group = QGroupBox("4. Обработка")
        process_layout = QVBoxLayout()
        
        batch_btn = QPushButton("Массовая обработка")
        batch_btn.clicked.connect(self.open_batch_processor)
        process_layout.addWidget(batch_btn)
        
        process_group.setLayout(process_layout)
        layout.addWidget(process_group)
        
        layout.addStretch()
        
        return panel
    
    def load_pdf(self):
        """Загрузить PDF файл"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите PDF файл",
            "",
            "PDF Files (*.pdf)"
        )
        
        if file_path:
            self.current_pdf_path = file_path
            self.pdf_label.setText(f"Загружен: {os.path.basename(file_path)}")
            self.statusBar().showMessage(f"Загружен: {file_path}")
            
            # Обновляем предварительный просмотр
            self.preview_widget.load_pdf(file_path)
            
            # Обновляем максимальную страницу
            from core.pdf_handler import PDFHandler
            page_count = PDFHandler.get_page_count(file_path)
            self.page_spin.setMaximum(page_count - 1)
    
    def on_position_changed(self):
        """Обработчик изменения позиции"""
        self.current_position.page = self.page_spin.value()
        self.current_position.x = self.x_spin.value()
        self.current_position.y = self.y_spin.value()
        self.current_position.width = self.width_spin.value()
        self.current_position.height = self.height_spin.value()
        
        # Обновляем предварительный просмотр
        self.preview_widget.update_signature_position(self.current_position)
    
    def open_signature_manager(self):
        """Открыть менеджер подписей"""
        dialog = SignatureManagerDialog(self)
        dialog.exec_()
    
    def open_batch_processor(self):
        """Открыть окно массовой обработки"""
        if not self.current_pdf_path:
            QMessageBox.warning(self, "Ошибка", "Сначала загрузите PDF файл")
            return
        
        dialog = BatchProcessorDialog(
            self.current_pdf_path,
            self.current_position,
            self
        )
        dialog.exec_()