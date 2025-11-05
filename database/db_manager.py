import sqlite3
from config.settings import DATABASE_PATH
from database.models import Person
from datetime import datetime

class DatabaseManager:
    """Менеджер для работы с базой данных"""
    
    def __init__(self):
        self.db_path = DATABASE_PATH
    
    def get_connection(self):
        """Получить соединение с БД"""
        return sqlite3.connect(self.db_path)
    
    def initialize(self):
        """Инициализация базы данных"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Создание таблицы людей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS persons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                position TEXT,
                signature_path TEXT NOT NULL,
                date_added TEXT NOT NULL
            )
        ''')
        
        # Создание таблицы шаблонов позиций
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS position_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                x REAL NOT NULL,
                y REAL NOT NULL,
                width REAL NOT NULL,
                height REAL NOT NULL,
                page INTEGER NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_person(self, person):
        """Добавить человека в БД"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO persons (name, position, signature_path, date_added)
            VALUES (?, ?, ?, ?)
        ''', (person.name, person.position, person.signature_path, person.date_added))
        
        person_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return person_id
    
    def get_all_persons(self):
        """Получить всех людей из БД"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, name, position, signature_path, date_added FROM persons')
        rows = cursor.fetchall()
        conn.close()
        
        persons = []
        for row in rows:
            person = Person(
                id=row[0],
                name=row[1],
                position=row[2],
                signature_path=row[3],
                date_added=row[4]
            )
            persons.append(person)
        
        return persons
    
    def get_person_by_id(self, person_id):
        """Получить человека по ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, name, position, signature_path, date_added FROM persons WHERE id = ?', (person_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Person(
                id=row[0],
                name=row[1],
                position=row[2],
                signature_path=row[3],
                date_added=row[4]
            )
        return None
    
    def update_person(self, person):
        """Обновить данные человека"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE persons
            SET name = ?, position = ?, signature_path = ?
            WHERE id = ?
        ''', (person.name, person.position, person.signature_path, person.id))
        
        conn.commit()
        conn.close()
    
    def delete_person(self, person_id):
        """Удалить человека из БД"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM persons WHERE id = ?', (person_id,))
        
        conn.commit()
        conn.close()
    
    def save_position_template(self, name, position):
        """Сохранить шаблон позиции"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO position_templates (name, x, y, width, height, page)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, position.x, position.y, position.width, position.height, position.page))
        
        conn.commit()
        conn.close()
    
    def get_position_templates(self):
        """Получить все шаблоны позиций"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, name, x, y, width, height, page FROM position_templates')
        rows = cursor.fetchall()
        conn.close()
        
        return [(row[0], row[1], {'x': row[2], 'y': row[3], 'width': row[4], 'height': row[5], 'page': row[6]}) for row in rows]