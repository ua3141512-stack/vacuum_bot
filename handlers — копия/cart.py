from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.inline import get_cart_keyboard
from data.db import get_products

router = Router()

# A simple in-memory cart for demonstration. In production, use Redis or a DB.
# Structure: {user_id: {product_id: quantity}}
user_carts = {}

@router.callback_query(F.data.startswith("add_"))
async def add_to_cart(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id
    
    if user_id not in user_carts:
        user_carts[user_id] = {}
        
    if product_id in user_carts[user_id]:
        user_carts[user_id][product_id] += 1
    else:
        user_carts[user_id][product_id] = 1
        
    await callback.answer("✅ Mahsulot savatchaga qo'shildi!", show_alert=True)

@router.message(F.text == "🛒 Savatcha")
async def view_cart(message: Message):
    user_id = message.from_user.id
    cart = user_carts.get(user_id, {})
    
    if not cart:
        await message.answer("Savatchangiz bo'sh. 🛒")
        return
        
    text = "🛒 <b>Sizning savatchangiz:</b>\n\n"
    total_price = 0
    products_data = get_products()
    
    for p_id, qty in cart.items():
        product = next((p for p in products_data if p['id'] == p_id), None)
        if product:
            item_total = product['price'] * qty
            total_price += item_total
            text += f"▪️ {product['name']} x {qty} = {item_total:,.0f} so'm\n"
            
    text += f"\n<b>Umumiy summa: {total_price:,.0f} so'm</b>"
    
    await message.answer(text, parse_mode="HTML", reply_markup=get_cart_keyboard())

@router.callback_query(F.data == "clear_cart")
async def clear_cart(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in user_carts:
        user_carts.pop(user_id)
    await callback.message.edit_text("Savatcha tozalandi. 🗑")
    await callback.answer()
