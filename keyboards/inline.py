from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_catalog_categories(categories: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for category in categories:
        builder.button(text=category, callback_data=f"category_{category}")
    builder.adjust(1)
    return builder.as_markup()

def get_products_keyboard(products: list[dict], category: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for product in products:
        if product['category'] == category:
            builder.button(text=product['name'], callback_data=f"product_{product['id']}")
    builder.button(text="🔙 Orqaga", callback_data="back_to_categories")
    builder.adjust(1)
    return builder.as_markup()

def get_product_action_keyboard(product_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="➕ Savatchaga qo'shish", callback_data=f"add_{product_id}")
    builder.button(text="🔙 Orqaga", callback_data="back_to_products")
    builder.adjust(1)
    return builder.as_markup()

def get_cart_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Buyurtmani rasmiylashtirish", callback_data="checkout")
    builder.button(text="❌ Tozalash", callback_data="clear_cart")
    builder.adjust(1)
    return builder.as_markup()
