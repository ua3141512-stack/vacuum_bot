import os
from aiogram import Router, F
from aiogram.types import Message
from google import genai
from config import config

router = Router()

@router.message(F.text)
async def handle_ai_query(message: Message):
    if not config.gemini_api_key:
        return
    
    try:
        client = genai.Client(api_key=config.gemini_api_key)
        prompt = f"Sen Aura Roboclean va maishiy texnikalar bo'yicha ekspert va sotuvchisan. O'zbek tilida qisqa va foydali javob ber. Savol: {message.text}"
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        await message.answer(response.text)
    except Exception as e:
        await message.answer("Uzur, hozir AI tizimida xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko'ring.")
