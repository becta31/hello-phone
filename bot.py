import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from openai import AsyncOpenAI

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_TEXT = os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini")
MODEL_IMAGE = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-1")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Напиши, что приготовить, и я пришлю рецепт + картинку.")

@dp.message(F.text)
async def recipe(message: Message):
    text = message.text.strip()
    r = await client.responses.create(model=MODEL_TEXT, input=f"Сделай рецепт: {text}")
    recipe_text = r.output_text.strip()
    await message.answer(recipe_text)

    img = await client.images.generate(
        model=MODEL_IMAGE,
        prompt=f"Реалистичное фото блюда по рецепту: {recipe_text[:400]}",
        size="1024x1024",
    )
    await message.answer(f"Картинка сгенерирована ✅ (base64 length: {len(img.data[0].b64_json)})")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
