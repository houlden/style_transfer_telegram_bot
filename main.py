import os

from bot_init import bot, dp, storage
from aiogram import executor
from config import ADMIN_ID
import handlers  # Запуск хэндлеров


async def on_startup(_):
    await bot.send_message(chat_id=ADMIN_ID, text='Бот запущен')
    await bot.set_webhook()


async def on_shutdown(_):
    await bot.send_message(chat_id=ADMIN_ID, text='Бот выключен')
    await storage.close()
    await bot.delete_webhook()


if __name__ == '__main__':
    # executor.start_polling(dispatcher=dp,
    #                        on_startup=on_startup,
    #                        on_shutdown=on_shutdown,
    #                        skip_updates=True)
    executor.start_webhook(dispatcher=dp,
                           webhook_path='',
                           on_startup=on_startup,
                           on_shutdown=on_shutdown,
                           skip_updates=True,
                           host='0.0.0.0',
                           port=int(os.environ.get('PORT', 5000)))
