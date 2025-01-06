from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.handlers import message
from aiogram.types import CallbackQuery
from datetime import datetime, timedelta

from config import load_config
from handlers.get_report_fromWB import get_sales_report
from states import ReportStates
from keyboards import generate_shop_keyboard, report_period_keyboard, main_menu_keyboard

router = Router()
config = load_config()


@router.message(Command('report'))
async def choose_shop(message: types.Message):
    if not config:
        await message.answer("Нет сохраненных магазинов. Сначала добавьте магазин.")
        return

    keyboard = generate_shop_keyboard(config.keys())
    await message.answer("Выберите магазин для отчета:", reply_markup=keyboard)


@router.callback_query(lambda callback: callback.data.startswith('shop_'))
async def choose_report_period(callback_query: CallbackQuery, state: FSMContext):
    shop_name = callback_query.data.split("_")[-1]
    await state.update_data(shop_name=shop_name)

    keyboard = report_period_keyboard()
    await callback_query.message.answer(
        f'Вы выбрали магазин "{shop_name}". Теперь выберите период отчёта:',
        reply_markup=keyboard
    )


@router.callback_query(lambda callback: callback.data.startswith('period_'))
async def handle_period_choice(callback_query: CallbackQuery, state: FSMContext):
    period = callback_query.data.split("_")[-1]
    data = await state.get_data()
    shop_name = data.get("shop_name")
    today = datetime.today().date()

    if period == "today":
        start_date = today
        end_date = today
    elif period == "yesterday":
        start_date = today - timedelta(days=1)
        end_date = today - timedelta(days=1)
    elif period == "last7":
        start_date = today - timedelta(days=7)
        end_date = today
    elif period == "custom":
        await callback_query.message.answer("Введите дату начала в формате ГГГГ-MM-ДД:")
        await state.set_state(ReportStates.waiting_for_start_date)
        return

    API_KEY = config.get(shop_name, {}).get('api_key')
    sales_data = get_sales_report(API_KEY, start_date.isoformat(), end_date.isoformat())

    total_sales = sum(item.get('priceWithDisc', 0) for item in sales_data)
    total_commission = sum(item.get('forPay', 0) for item in sales_data)
    total_discounts = sum(item.get('discount', 0) for item in sales_data)
    total_logistics = sum(item.get('logisticsCost', 0) for item in sales_data)
    total_storage = sum(item.get('storageCost', 0) for item in sales_data)
    total_units_sold = sum(item.get('quantity', 0) for item in sales_data)

    report = (
        f"Отчет за период с {start_date} по {end_date} для магазина '{shop_name}':\n\n"
        f"🔹 Общая сумма продаж: {total_sales} руб.\n"
        f"🔹 Комиссия Wildberries: {total_commission} руб.\n"
        f"🔹 Скидки Wildberries: {total_discounts} руб.\n"
        f"🔹 Комиссия эквайринга: {total_commission * 0.02} руб. (примерная)\n"
        f"🔹 Стоимость логистики: {total_logistics} руб.\n"
        f"🔹 Стоимость хранения: {total_storage} руб.\n"
        f"🔹 Количество проданных единиц: {total_units_sold}\n"
    )

    await callback_query.message.answer(report)
    await message.answer(reply_markup=main_menu_keyboard())
    await state.clear()
