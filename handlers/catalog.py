from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.inline import get_catalog_categories, get_products_keyboard, get_product_action_keyboard
from data.db import get_products

router = Router()

@router.message(F.text == "📦 Mahsulotlar katalogi")
async def show_catalog(message: Message):
    products_data = get_products()
    categories = list(set([p.get('category', 'Boshqa') for p in products_data]))
    await message.answer("Qaysi turdagi changyutgich kerak?", reply_markup=get_catalog_categories(categories))

@router.callback_query(F.data.startswith("category_"))
async def show_category_products(callback: CallbackQuery):
    category = callback.data.split("_", 1)[1]
    products_data = get_products()
    await callback.message.edit_text(
        f"Kategoriya: {category}\nMahsulotni tanlang:",
        reply_markup=get_products_keyboard(products_data, category)
    )

@router.callback_query(F.data == "back_to_categories")
async def back_to_categories(callback: CallbackQuery):
    products_data = get_products()
    categories = list(set([p.get('category', 'Boshqa') for p in products_data]))
    await callback.message.edit_text("Qaysi turdagi changyutgich kerak?", reply_markup=get_catalog_categories(categories))

@router.callback_query(F.data.startswith("product_"))
async def show_product_details(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    products_data = get_products()
    product = next((p for p in products_data if p['id'] == product_id), None)
    
    if product:
        text = (
            f"<b>{product['name']}</b>\n\n"
            f"{product['description']}\n\n"
            f"Narxi: {product['price']:,.0f} so'm"
        )
        await callback.message.delete()
        if product.get('image_url') and str(product['image_url']).startswith('http') or len(str(product.get('image_url', ''))) > 20:
            await callback.message.answer_photo(
                photo=product['image_url'],
                caption=text,
                parse_mode="HTML",
                reply_markup=get_product_action_keyboard(product_id)
            )
        else:
            await callback.message.answer(text, parse_mode="HTML", reply_markup=get_product_action_keyboard(product_id))

@router.callback_query(F.data == "back_to_products")
async def back_to_products_from_details(callback: CallbackQuery):
    products_data = get_products()
    categories = list(set([p.get('category', 'Boshqa') for p in products_data]))
    await callback.message.delete()
    await callback.message.answer("Qaysi turdagi changyutgich kerak?", reply_markup=get_catalog_categories(categories))
