from aiogram.filters import Command

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from config import load_config, save_config
from keyboards import main_menu_keyboard
from states import DelShopStates

router = Router()


@router.message(Command("delshop"))
async def del_shop(message: types.Message, state: FSMContext):
    config = load_config()
    if not config:
        await message.answer("У вас нет сохраненных магазинов")
        return

    shop_names = "\n".join(config.keys())
    await message.answer(f"Сохраненные магазины:\n{shop_names}\n\nВведите название магазина для удаления:")
    await state.set_state(DelShopStates.waiting_for_shop_name)


@router.message(DelShopStates.waiting_for_shop_name)
async def confirm_delete_shop(message: types.Message, state: FSMContext):
    shop_name = message.text
    config = load_config()

    if shop_name not in config:
        await message.answer(f"Магазин с именем '{shop_name}' не найден.")
        await state.clear()
        return

    await state.update_data(shop_name=shop_name)
    await message.answer(f"Вы уверены, что хотите удалить магазин '{shop_name}'\n Hапишите 'Да' для подтверждения.")
    await state.set_state(DelShopStates.confirming_deletion)


@router.message(DelShopStates.confirming_deletion)
async def delete_shop_from_config(message: types.Message, state: FSMContext):
    if message.text.strip().lower() == "да":
        data = await state.get_data()
        shop_name = data["shop_name"]

        config = load_config()
        del config[shop_name]
        save_config(config)

        await message.answer(f"Магазин '{shop_name}' успешно удален!")
    else:
        await message.answer("Удаление передумано)")
    await message.answer(reply_markup=main_menu_keyboard())
    await state.clear()
