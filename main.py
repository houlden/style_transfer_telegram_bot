from bot_init import bot, dp, storage
from aiogram import executor
from config import ADMIN_ID, WEBHOOK_URL, WEBHOOK_PATH, HOST, PORT
import handlers  # Запуск хэндлеров через init пакета (возможно лучше было вызывать их явно из main, не уверен)


async def on_startup(_):
    """
    Срабатывает во время запуска бота.
    """
    await bot.send_message(chat_id=ADMIN_ID, text='Бот запущен')
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(_):
    """
    Срабатывает при завершении работы бота.
    """
    await bot.send_message(chat_id=ADMIN_ID, text='Бот выключен')
    await storage.close()
    # await bot.delete_webhook()


if __name__ == '__main__':
    # executor.start_polling(dispatcher=dp,
    #                        on_startup=on_startup,
    #                        on_shutdown=on_shutdown,
    #                        skip_updates=True)
    executor.start_webhook(dispatcher=dp,
                           webhook_path=WEBHOOK_PATH,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown,
                           skip_updates=True,
                           host=HOST,
                           port=PORT)
