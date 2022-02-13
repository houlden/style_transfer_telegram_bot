from bot_init import bot, dp, storage
from aiogram import executor
from config import ADMIN_ID
import handlers  # Запуск хэндлеров


async def on_startup(_):
    await bot.send_message(chat_id=ADMIN_ID, text='Бот запущен')


async def on_shutdown(_):
    await storage.close()
    await bot.send_message(chat_id=ADMIN_ID, text='Бот выключен')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
