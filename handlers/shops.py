from aiogram.filters import Command

from aiogram import Router, types

from config import load_config
from keyboards import main_menu_keyboard

router = Router()


@router.message(Command("shop_list"))
async def list_shops(message: types.Message):
    config = load_config()
    if not config:
        await message.answer('У вас нет магазинов, попробуйте добавить командой /addshop')
        return

    shop_names = "\n".join(config.keys())
    await message.answer(f"Список ваших магазинов:\n{shop_names}")
    await message.answer("Выберите дальнейшее действие:", reply_markup=main_menu_keyboard())