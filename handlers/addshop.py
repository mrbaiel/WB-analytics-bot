from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from config import load_config, save_config
from keyboards import main_menu_keyboard
from states import AddShopStates

router = Router()

@router.message(Command("addshop"))
async def start_add_shop(message: types.Message, state: FSMContext):
    await message.answer("Введите название магазина:")
    await state.set_state(AddShopStates.waiting_for_shop_name)

@router.message(AddShopStates.waiting_for_shop_name)
async def add_shop_name(message: types.Message, state: FSMContext):
    shop_name = message.text.strip()
    await state.update_data(shop_name=shop_name)
    await message.answer("Введите API-ключ для магазина:")
    await state.set_state(AddShopStates.waiting_for_api_key)

@router.message(AddShopStates.waiting_for_api_key)
async def add_shop_api_key(message: types.Message, state: FSMContext):
    api_key = message.text.strip()
    data = await state.get_data()

    shop_name = data["shop_name"]
    config = load_config()
    config[shop_name] = {"api_key": api_key}
    save_config(config)

    await message.answer(f"Магазин '{shop_name}' успешно добавлен!", reply_markup=ReplyKeyboardRemove())
    await state.clear()

    await message.answer("Выберите дальнейшее действие:", reply_markup=main_menu_keyboard())
