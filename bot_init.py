from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN


# Заведем хранилище в RAM для передачи информации между состояниями
storage = MemoryStorage()

bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot=bot, storage=storage)
