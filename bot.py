import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from decouple import config

from handlers import addshop, delshop, shops, report
from keyboards import main_menu_keyboard

API_TOKEN = config('API_TOKEN')

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

# Регистрация всех роутеров
dp.include_router(addshop.router)
dp.include_router(delshop.router)
dp.include_router(shops.router)
dp.include_router(report.router)

# Обработчик команды /start
@dp.message(Command("start"))
async def show_main_menu(message: Message):
    """Главное меню."""
    await message.answer("Выберите действие:", reply_markup=main_menu_keyboard())

# Запуск бота
if __name__ == "__main__":
    import asyncio

    async def main():
        print("Бот запущен!")
        await dp.start_polling(bot)

    asyncio.run(main())
