import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import config
from handlers import start, catalog, cart, order, admin, ai_assistant

async def main():
    logging.basicConfig(level=logging.INFO)
    
    bot = Bot(token=config.bot_token)
    dp = Dispatcher()
    
    dp.include_routers(
        admin.router,
        start.router,
        catalog.router,
        cart.router,
        order.router,
        ai_assistant.router
    )
    
    print("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
