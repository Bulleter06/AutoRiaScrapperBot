import asyncio
import os
from pathlib import Path
from aiogram import Bot
from scrapper import fetch_autoria_listings, parse_listings
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

API_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not API_TOKEN:
    raise ValueError("BOT_TOKEN is missing! Check your .env file.")
if not CHAT_ID:
    raise ValueError("CHAT_ID is missing! Check your .env file.")

bot = Bot(token=API_TOKEN)

async def send_listings():
    html = fetch_autoria_listings()
    listings = parse_listings(html)

    if not listings:
        await bot.send_message(CHAT_ID, "⚠️ Не знайдено жодного оголошення.")
    else:
        for item in listings:
            text = (
                f"🚗 Нове оголошення:\n\n"
                f"🔹 {item['title']}\n"
                f"💰 {item['price']}\n"
                f"🔗 {item['link']}"
            )
            await bot.send_message(CHAT_ID, text)

    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(send_listings())
