from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox,
                             QLineEdit, QLabel, QGroupBox, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from database.db_manager import DatabaseManager
from database.models import Person
from utils.file_utils import FileUtils
from utils.validators import Validators
import os

class SignatureManagerDialog(QDialog):
    """Диалог управления подписями"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_manager = DatabaseManager()
        self.file_utils = FileUtils()
        self.validators = Validators()
        
        self.init_ui()
        self.load_persons()
    
    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle("Управление подписями")
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout(self)
        
        # Форма добавления
        add_group = QGroupBox("Добавить нового человека")
        add_layout = QVBoxLayout()
        
        # Имя
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("ФИО:"))
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_input)
        add_layout.addLayout(name_layout)
        
        # Должность
        position_layout = QHBoxLayout()
        position_layout.addWidget(QLabel("Должность:"))
        self.position_input = QLineEdit()
        position_layout.addWidget(self.position_input)
        add_layout.addLayout(position_layout)
        
        # Подпись
        signature_layout = QHBoxLayout()
        signature_layout.addWidget(QLabel("Подпись:"))
        self.signature_path_label = QLabel("Не выбрана")
        signature_layout.addWidget(self.signature_path_label)
        select_sig_btn = QPushButton("Выбрать файл")
        select_sig_btn.clicked.connect(self.select_signature_file)
        signature_layout.addWidget(select_sig_btn)
        add_layout.addLayout(signature_layout)
        
        # Кнопка добавления
        add_btn = QPushButton("Добавить")
        add_btn.clicked.connect(self.add_person)
        add_layout.addWidget(add_btn)
        
        add_group.setLayout(add_layout)
        layout.addWidget(add_group)
        
        # Таблица с людьми
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "ФИО", "Должность", "Подпись"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        view_btn = QPushButton("Просмотр подписи")
        view_btn.clicked.connect(self.view_signature)
        buttons_layout.addWidget(view_btn)
        
        delete_btn = QPushButton("Удалить")
        delete_btn.clicked.connect(self.delete_person)
        buttons_layout.addWidget(delete_btn)
        
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(close_btn)
        
        layout.addLayout(buttons_layout)
        
        self.selected_signature_path = None
    
    def select_signature_file(self):
        """Выбрать файл подписи"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл подписи",
            "",
            "Image Files (*.png *.jpg *.jpeg)"
        )
        
        if file_path:
            valid, message = self.validators.validate_signature_file(file_path)
            if not valid:
                QMessageBox.warning(self, "Ошибка", message)
                return
            
            self.selected_signature_path = file_path
            self.signature_path_label.setText(os.path.basename(file_path))
    
    def add_person(self):
        """Добавить человека"""
        name = self.name_input.text().strip()
        position = self.position_input.text().strip()
        
        # Валидация
        valid, message = self.validators.validate_person_name(name)
        if not valid:
            QMessageBox.warning(self, "Ошибка", message)
            return
        
        if not self.selected_signature_path:
            QMessageBox.warning(self, "Ошибка", "Выберите файл подписи")
            return
        
        try:
            # Копируем файл подписи
            signature_path = self.file_utils.copy_signature_file(
                self.selected_signature_path,
                name
            )
            
            # Создаем объект Person
            person = Person(
                name=name,
                position=position,
                signature_path=signature_path
            )
            
            # Сохраняем в БД
            self.db_manager.add_person(person)
            
            # Очищаем форму
            self.name_input.clear()
            self.position_input.clear()
            self.signature_path_label.setText("Не выбрана")
            self.selected_signature_path = None
            
            # Обновляем таблицу
            self.load_persons()
            
            QMessageBox.information(self, "Успех", f"Человек {name} добавлен")
        
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка добавления: {str(e)}")
    
    def load_persons(self):
        """Загрузить список людей"""
        persons = self.db_manager.get_all_persons()
        
        self.table.setRowCount(len(persons))
        
        for i, person in enumerate(persons):
            self.table.setItem(i, 0, QTableWidgetItem(str(person.id)))
            self.table.setItem(i, 1, QTableWidgetItem(person.name))
            self.table.setItem(i, 2, QTableWidgetItem(person.position))
            self.table.setItem(i, 3, QTableWidgetItem(os.path.basename(person.signature_path)))
    
    def view_signature(self):
        """Просмотреть подпись"""
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите человека из списка")
            return
        
        person_id = int(self.table.item(selected[0].row(), 0).text())
        person = self.db_manager.get_person_by_id(person_id)
        
        if person and os.path.exists(person.signature_path):
            # Создаем диалог для просмотра
            dialog = QDialog(self)
            dialog.setWindowTitle(f"Подпись: {person.name}")
            layout = QVBoxLayout(dialog)
            
            label = QLabel()
            pixmap = QPixmap(person.signature_path)
            label.setPixmap(pixmap.scaled(400, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            layout.addWidget(label)
            
            close_btn = QPushButton("Закрыть")
            close_btn.clicked.connect(dialog.accept)
            layout.addWidget(close_btn)
            
            dialog.exec_()
        else:
            QMessageBox.warning(self, "Ошибка", "Файл подписи не найден")
    
    def delete_person(self):
        """Удалить человека"""
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите человека из списка")
            return
        
        person_id = int(self.table.item(selected[0].row(), 0).text())
        person = self.db_manager.get_person_by_id(person_id)
        
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            f"Удалить {person.name}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Удаляем файл подписи
                if os.path.exists(person.signature_path):
                    self.file_utils.delete_signature_file(person.signature_path)
                
                # Удаляем из БД
                self.db_manager.delete_person(person_id)
                
                # Обновляем таблицу
                self.load_persons()
                
                QMessageBox.information(self, "Успех", "Человек удален")
            
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка удаления: {str(e)}")