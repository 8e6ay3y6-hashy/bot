import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
import yt_dlp

TOKEN = "8791827254:AAE7TNX82Yb80sIKX1kG0WFkb..."

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("سڵاو! 👋\n\nمن بۆتی دابەزاندنی ڤیدیۆم.\nلینکی یوتیوب یان اینستاگرام بۆ بنێرە!")

@dp.message(F.text.startswith("http"))
async def download_video(message: types.Message):
    url = message.text.strip()
    processing_msg = await message.answer("⏳ چاوەڕێ بکە...")

    output_file = f"video_{message.from_user.id}.mp4"
    ydl_opts = {'outtmpl': output_file, 'format': 'best', 'noplaylist': True}

    try:
        def download():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        await asyncio.to_thread(download)

        if os.path.exists(output_file):
            await message.answer_video(types.FSInputFile(output_file))
            os.remove(output_file)
            await bot.delete_message(chat_id=message.chat.id, message_id=processing_msg.message_id)
        else:
            await message.answer("❌ ڤیدیۆکە نەدۆزرایەوە.")
            await bot.delete_message(chat_id=message.chat.id, message_id=processing_msg.message_id)
    except Exception as e:
        await message.answer("❌ هەڵەیەک ڕوویدا.")
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=processing_msg.message_id)
        except:
            pass

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
