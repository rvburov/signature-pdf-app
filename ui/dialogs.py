from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class AboutDialog(QDialog):
    """Диалог О программе"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle("О программе")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout(self)
        
        title = QLabel("PDF Signature Tool")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        version = QLabel("Версия 1.0.0")
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)
        
        description = QLabel(
            "Программа для автоматической подстановки\n"
            "подписей в PDF документы.\n\n"
            "Возможности:\n"
            "- Управление базой подписей\n"
            "- Настройка позиции подписи\n"
            "- Массовая обработка документов"
        )
        description.setAlignment(Qt.AlignCenter)
        description.setWordWrap(True)
        layout.addWidget(description)
        
        layout.addStretch()
        
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)


class ErrorDialog(QDialog):
    """Диалог для отображения ошибок"""
    
    def __init__(self, title, message, details=None, parent=None):
        super().__init__(parent)
        self.init_ui(title, message, details)
    
    def init_ui(self, title, message, details):
        """Инициализация интерфейса"""
        self.setWindowTitle(title)
        self.setMinimumSize(400, 200)
        
        layout = QVBoxLayout(self)
        
        msg_label = QLabel(message)
        msg_label.setWordWrap(True)
        layout.addWidget(msg_label)
        
        if details:
            details_label = QLabel(f"\nПодробности:\n{details}")
            details_label.setWordWrap(True)
            details_label.setStyleSheet("color: red; font-size: 10px;")
            layout.addWidget(details_label)
        
        layout.addStretch()
        
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)


def show_info(parent, title, message):
    """Показать информационное сообщение"""
    QMessageBox.information(parent, title, message)


def show_warning(parent, title, message):
    """Показать предупреждение"""
    QMessageBox.warning(parent, title, message)


def show_error(parent, title, message, details=None):
    """Показать ошибку"""
    if details:
        dialog = ErrorDialog(title, message, details, parent)
        dialog.exec_()
    else:
        QMessageBox.critical(parent, title, message)


def ask_question(parent, title, question):
    """Задать вопрос пользователю"""
    reply = QMessageBox.question(
        parent,
        title,
        question,
        QMessageBox.Yes | QMessageBox.No
    )
    return reply == QMessageBox.Yes