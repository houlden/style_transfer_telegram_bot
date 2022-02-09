from bot_init import bot, dp
from aiogram import executor
from config import ADMIN_ID
import handlers


async def on_startup(_):
    await bot.send_message(chat_id=ADMIN_ID, text='Бот запущен')

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
