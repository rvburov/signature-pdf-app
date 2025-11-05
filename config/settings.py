import os

# Пути к директориям
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
SIGNATURES_DIR = os.path.join(DATA_DIR, 'signatures')
TEMPLATES_DIR = os.path.join(DATA_DIR, 'templates')
OUTPUT_DIR = os.path.join(DATA_DIR, 'output')
DATABASE_PATH = os.path.join(DATA_DIR, 'database.db')

# Настройки приложения
APP_NAME = "PDF Signature Tool"
APP_VERSION = "1.0.0"

# Настройки PDF
DEFAULT_DPI = 72
PDF_QUALITY = 95

# Поддерживаемые форматы
SUPPORTED_IMAGE_FORMATS = ['.png', '.jpg', '.jpeg']
SUPPORTED_PDF_FORMATS = ['.pdf']

# Настройки UI
WINDOW_MIN_WIDTH = 1000
WINDOW_MIN_HEIGHT = 700
PREVIEW_MAX_WIDTH = 800
PREVIEW_MAX_HEIGHT = 1000

# Настройки подписи
DEFAULT_SIGNATURE_WIDTH = 150
DEFAULT_SIGNATURE_HEIGHT = 50