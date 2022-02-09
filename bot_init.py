from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN


storage = MemoryStorage()

bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot=bot, storage=storage)
