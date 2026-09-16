from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from states.order_state import OrderState
from keyboards.reply import get_contact_keyboard, get_location_keyboard, get_main_menu
from handlers.cart import user_carts
from data.db import get_products
from config import config

router = Router()

@router.callback_query(F.data == "checkout")
async def start_checkout(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if user_id not in user_carts or not user_carts[user_id]:
        await callback.answer("Savatchangiz bo'sh!", show_alert=True)
        return
        
    await state.set_state(OrderState.waiting_for_name)
    await callback.message.answer("Iltimos, ismingizni kiriting:", reply_markup=ReplyKeyboardRemove())
    await callback.answer()

@router.message(OrderState.waiting_for_name, F.text)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(OrderState.waiting_for_phone)
    await message.answer("Telefon raqamingizni yuboring:", reply_markup=get_contact_keyboard())

@router.message(OrderState.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text
        
    await state.update_data(phone=phone)
    await state.set_state(OrderState.waiting_for_address)
    await message.answer("Yetkazib berish manzilini yuboring yoki matn ko'rinishida kiriting:", reply_markup=get_location_keyboard())

@router.message(OrderState.waiting_for_address)
async def process_address(message: Message, state: FSMContext):
    if message.location:
        address = f"Kenglik: {message.location.latitude}, Uzunlik: {message.location.longitude}"
    else:
        address = message.text
        
    user_data = await state.get_data()
    user_id = message.from_user.id
    cart = user_carts.get(user_id, {})
    
    # Format order summary
    order_details = ""
    total_price = 0
    products_data = get_products()
    for p_id, qty in cart.items():
        product = next((p for p in products_data if p['id'] == p_id), None)
        if product:
            item_total = product['price'] * qty
            total_price += item_total
            order_details += f"- {product['name']} (x{qty})\n"
            
    admin_msg = (
        f"🚨 <b>YANGI BUYURTMA</b> 🚨\n\n"
        f"👤 <b>Mijoz:</b> {user_data['name']}\n"
        f"📞 <b>Tel:</b> {user_data['phone']}\n"
        f"📍 <b>Manzil:</b> {address}\n\n"
        f"📦 <b>Buyurtma tarkibi:</b>\n{order_details}\n"
        f"💰 <b>Umumiy summa:</b> {total_price:,.0f} so'm\n"
        f"🆔 User ID: {user_id}"
    )
    
    # Notify admins
    for admin_id in config.admins:
        try:
            await message.bot.send_message(chat_id=admin_id, text=admin_msg, parse_mode="HTML")
        except Exception as e:
            print(f"Error sending to admin {admin_id}: {e}")
            
    # Clear cart and finish
    user_carts.pop(user_id, None)
    await state.clear()
    
    await message.answer(
        "✅ Buyurtmangiz muvaffaqiyatli qabul qilindi! Tez orada operatorlarimiz siz bilan bog'lanishadi.",
        reply_markup=get_main_menu()
    )
