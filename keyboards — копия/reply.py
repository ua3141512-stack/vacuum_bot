from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Mahsulotlar katalogi")],
            [KeyboardButton(text="🛒 Savatcha")],
            [KeyboardButton(text="ℹ️ Biz haqimizda va Kafolat"), KeyboardButton(text="📞 Aloqa / Qo'llab-quvvatlash")]
        ],
        resize_keyboard=True
    )

def get_contact_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]
        ],
        resize_keyboard=True
    )

def get_location_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Manzilni yuborish", request_location=True)]
        ],
        resize_keyboard=True
    )
