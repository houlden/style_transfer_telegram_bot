import os
from dotenv import load_dotenv


# Загрузка переменных из файла .env в переменные окружения
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

WEBHOOK_URL = os.getenv('WEBHOOK_URL')
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH')
WEBAPP_HOST = os.getenv('WEBAPP_HOST')
WEBAPP_PORT = int(os.environ.get('PORT', 5000))

EXAMPLE_PATH_GATYS = 'examples/nst_gatys/results.jpg'
