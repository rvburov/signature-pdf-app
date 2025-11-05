from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QListWidget, QLabel, QProgressBar, QMessageBox,
                             QListWidgetItem, QAbstractItemView)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from database.db_manager import DatabaseManager
from core.signature_processor import SignatureProcessor
import os

class BatchProcessorDialog(QDialog):
    """Диалог массовой обработки документов"""
    
    def __init__(self, pdf_path, position, parent=None):
        super().__init__(parent)
        self.pdf_path = pdf_path
        self.position = position
        self.db_manager = DatabaseManager()
        
        self.init_ui()
        self.load_persons()
    
    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle("Массовая обработка")
        self.setMinimumSize(600, 500)
        
        layout = QVBoxLayout(self)
        
        # Информация о PDF
        info_label = QLabel(f"PDF: {os.path.basename(self.pdf_path)}")
        layout.addWidget(info_label)
        
        # Инструкция
        instruction = QLabel("Выберите людей для создания документов:")
        layout.addWidget(instruction)
        
        # Список людей
        self.persons_list = QListWidget()
        self.persons_list.setSelectionMode(QAbstractItemView.MultiSelection)
        layout.addWidget(self.persons_list)
        
        # Прогресс бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Статус
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        select_all_btn = QPushButton("Выбрать всех")
        select_all_btn.clicked.connect(self.select_all)
        buttons_layout.addWidget(select_all_btn)
        
        deselect_all_btn = QPushButton("Снять выделение")
        deselect_all_btn.clicked.connect(self.deselect_all)
        buttons_layout.addWidget(deselect_all_btn)
        
        self.process_btn = QPushButton("Обработать")
        self.process_btn.clicked.connect(self.start_processing)
        buttons_layout.addWidget(self.process_btn)
        
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(close_btn)
        
        layout.addLayout(buttons_layout)
    
    def load_persons(self):
        """Загрузить список людей"""
        persons = self.db_manager.get_all_persons()
        
        for person in persons:
            item = QListWidgetItem(f"{person.name} ({person.position})")
            item.setData(Qt.UserRole, person)
            self.persons_list.addItem(item)
    
    def select_all(self):
        """Выбрать всех"""
        for i in range(self.persons_list.count()):
            self.persons_list.item(i).setSelected(True)
    
    def deselect_all(self):
        """Снять выделение"""
        self.persons_list.clearSelection()
    
    def start_processing(self):
        """Начать обработку"""
        selected_items = self.persons_list.selectedItems()
        
        if not selected_items:
            QMessageBox.warning(self, "Ошибка", "Выберите хотя бы одного человека")
            return
        
        # Получаем выбранных людей
        selected_persons = [item.data(Qt.UserRole) for item in selected_items]
        
        # Блокируем кнопки
        self.process_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(selected_persons))
        self.progress_bar.setValue(0)
        
        # Создаем и запускаем поток обработки
        self.worker = ProcessorWorker(self.pdf_path, selected_persons, self.position)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()
    
    def on_progress(self, current, total, name):
        """Обработчик прогресса"""
        self.progress_bar.setValue(current)
        self.status_label.setText(f"Обработка: {name} ({current}/{total})")
    
    def on_finished(self, output_files):
        """Обработчик завершения"""
        self.process_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"Готово! Создано файлов: {len(output_files)}")
        
        QMessageBox.information(
            self,
            "Успех",
            f"Обработка завершена!\nСоздано файлов: {len(output_files)}\nПапка: data/output/"
        )
    
    def on_error(self, error_message):
        """Обработчик ошибки"""
        self.process_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText("Ошибка обработки")
        
        QMessageBox.critical(self, "Ошибка", error_message)


class ProcessorWorker(QThread):
    """Рабочий поток для обработки документов"""
    
    progress = pyqtSignal(int, int, str)
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    
    def __init__(self, pdf_path, persons, position):
        super().__init__()
        self.pdf_path = pdf_path
        self.persons = persons
        self.position = position
        self.processor = SignatureProcessor()
    
    def run(self):
        """Запуск обработки"""
        try:
            output_files = self.processor.process_batch(
                self.pdf_path,
                self.persons,
                self.position,
                progress_callback=self.on_progress
            )
            self.finished.emit(output_files)
        
        except Exception as e:
            self.error.emit(str(e))
    
    def on_progress(self, current, total, name):
        """Обратный вызов прогресса"""
        self.progress.emit(current, total, name)