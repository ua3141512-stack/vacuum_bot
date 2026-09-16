from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.reply import get_main_menu

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        "Assalomu alaykum! Xush kelibsiz.\n\n"
        "Bizning bot orqali eng yaxshi maishiy texnika va changyutgichlarni (pelesoslarni) xarid qilishingiz mumkin. "
        "Marhamat, quyidagi menyudan kerakli bo'limni tanlang:"
    )
    await message.answer(welcome_text, reply_markup=get_main_menu())

@router.message(F.text == "ℹ️ Biz haqimizda va Kafolat")
async def about_and_warranty(message: Message):
    text = (
        "ℹ️ <b>Biz haqimizda:</b>\n"
        "Biz yillar davomida sifatli maishiy texnika va changyutgichlar sotuvini yo'lga qo'yganmiz.\n\n"
        "🛡 <b>Kafolat:</b>\n"
        "Barcha mahsulotlarimiz uchun rasmiy 1 yillik kafolat beriladi.\n\n"
        "🚚 <b>Yetkazib berish:</b>\n"
        "Respublika bo'ylab yetkazib berish xizmati mavjud. Toshkent shahri ichida yetkazib berish bepul."
    )
    await message.answer(text, parse_mode="HTML")

@router.message(F.text == "📞 Aloqa / Qo'llab-quvvatlash")
async def contact_support(message: Message):
    text = (
        "📞 <b>Aloqa uchun:</b>\n"
        "Telefon: +998 90 123 45 67\n"
        "Telegram: @admin_username\n"
        "Ish vaqti: 09:00 - 18:00 (Dushanba - Shanba)"
    )
    await message.answer(text, parse_mode="HTML")
