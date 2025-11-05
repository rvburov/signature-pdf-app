import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.main_window import MainWindow
from database.db_manager import DatabaseManager

def main():
    # Создание необходимых директорий
    os.makedirs('data/signatures', exist_ok=True)
    os.makedirs('data/templates', exist_ok=True)
    os.makedirs('data/output', exist_ok=True)
    os.makedirs('resources/icons', exist_ok=True)
    
    # Инициализация базы данных
    db = DatabaseManager()
    db.initialize()
    
    # Создание приложения
    app = QApplication(sys.argv)
    app.setApplicationName("PDF Signature Tool")
    
    # Включение High DPI
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Создание и показ главного окна
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()