from os import getenv
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN')
ADMIN_ID = getenv('ADMIN_ID')

# WEBHOOK_HOST = 'Ip вашего сервера'
# WEBHOOK_PATH = 'путь к апи где слушает ваш бот' #или пустое значение, если он слушает на стартовой странице.
# WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
#
# WEBAPP_HOST = '127.0.0.1'
# WEBAPP_PORT = 5000