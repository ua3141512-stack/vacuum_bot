from aiogram.fsm.state import State, StatesGroup

class AddProductState(StatesGroup):
    waiting_for_name = State()
    waiting_for_category = State()
    waiting_for_description = State()
    waiting_for_price = State()
    waiting_for_image = State()
