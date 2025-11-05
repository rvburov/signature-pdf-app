from datetime import datetime

class Person:
    """Модель для хранения информации о человеке"""
    
    def __init__(self, id=None, name='', position='', signature_path='', date_added=None):
        self.id = id
        self.name = name
        self.position = position
        self.signature_path = signature_path
        self.date_added = date_added or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position,
            'signature_path': self.signature_path,
            'date_added': self.date_added
        }
    
    @staticmethod
    def from_dict(data):
        return Person(
            id=data.get('id'),
            name=data.get('name', ''),
            position=data.get('position', ''),
            signature_path=data.get('signature_path', ''),
            date_added=data.get('date_added')
        )


class SignaturePosition:
    """Модель для позиции подписи на странице"""
    
    def __init__(self, x=0, y=0, width=150, height=50, page=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.page = page
    
    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'page': self.page
        }
    
    @staticmethod
    def from_dict(data):
        return SignaturePosition(
            x=data.get('x', 0),
            y=data.get('y', 0),
            width=data.get('width', 150),
            height=data.get('height', 50),
            page=data.get('page', 0)
        )