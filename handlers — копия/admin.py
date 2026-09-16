from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.admin_state import AddProductState
from data.db import save_product, get_products
from config import config

router = Router()

def is_admin(user_id: int) -> bool:
    return user_id in config.admins

@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.set_state(AddProductState.waiting_for_name)
    await message.answer("🛠 Yangi mahsulot qo'shish paneli:\n\nMahsulot nomini kiriting:")

@router.message(AddProductState.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddProductState.waiting_for_category)
    await message.answer("Mahsulot kategoriyasini kiriting (masalan: Suyuqlik so'ruvchi pelesoslar):")

@router.message(AddProductState.waiting_for_category)
async def process_category(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await state.set_state(AddProductState.waiting_for_description)
    await message.answer("Mahsulot tavsifini kiriting:")

@router.message(AddProductState.waiting_for_description)
async def process_desc(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddProductState.waiting_for_price)
    await message.answer("Mahsulot narxini kiriting (raqamlarda, masalan: 1500000):")

@router.message(AddProductState.waiting_for_price)
async def process_price(message: Message, state: FSMContext):
    try:
        price = int(message.text)
        await state.update_data(price=price)
        await state.set_state(AddProductState.waiting_for_image)
        await message.answer("Mahsulot rasmini (Photo) yuboring yoki rasm URLsini matn qilib jo'nating:")
    except ValueError:
        await message.answer("Iltimos, narxni faqat raqamlarda kiriting!")

@router.message(AddProductState.waiting_for_image)
async def process_image(message: Message, state: FSMContext):
    data = await state.get_data()
    image_url = ""
    
    if message.photo:
        image_url = message.photo[-1].file_id
    else:
        image_url = message.text

    products = get_products()
    new_id = max([p['id'] for p in products], default=0) + 1
    
    product = {
        "id": new_id,
        "name": data['name'],
        "category": data['category'],
        "description": data['description'],
        "price": data['price'],
        "image_url": image_url
    }
    
    save_product(product)
    await state.clear()
    await message.answer(f"✅ Mahsulot muvaffaqiyatli saqlandi!\nID: {new_id}\nNom: {product['name']}")
