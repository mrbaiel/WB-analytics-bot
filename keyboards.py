from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить магазин", callback_data="addshop")],
        [InlineKeyboardButton(text="❌ Удалить магазин", callback_data="delshop")],
        [InlineKeyboardButton(text="📋 Список магазинов", callback_data="shop_list")],
        [InlineKeyboardButton(text="📊 Отчёт", callback_data="report")],
    ])


def generate_shop_keyboard(shop_names: list) -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text=shop_name, callback_data=f"shop_{shop_name}")] for shop_name in shop_names]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def report_period_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="За сегодня", callback_data="period_today")],
        [InlineKeyboardButton(text="Вчера", callback_data="period_yesterday")],
        [InlineKeyboardButton(text="Последние 7 дней", callback_data="period_last7")],
        [InlineKeyboardButton(text="Указать вручную", callback_data="period_custom")]
    ])
