from aiogram.fsm.state import StatesGroup, State


class AddShopStates(StatesGroup):
    waiting_for_api_key = State()
    waiting_for_shop_name = State()

class DelShopStates(StatesGroup):
    waiting_for_shop_name = State()
    confirming_deletion = State()

class ReportStates(StatesGroup):
    waiting_for_start_date = State()
    waiting_for_end_date = State()