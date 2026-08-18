import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
import yt_dlp

TOKEN = "8791827254:AAE7TNx82Yb80sIKXlkG0WFKbpst_UwzG7Y"

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "سڵاو! 👋\n\n"
        "من بۆتی دابەزاندنی ڤیدیۆم.\n"
        "لینکی ئینستاگرام یان یوتیوب بۆ بنێرە تا بۆت دابەزێنم!"
    )

@dp.message(F.text.startswith("http"))
async def download_video(message: types.Message):
    url = message.text.strip()
    processing_msg = await message.answer("⏳ چاوەڕوان بن، ڤیدیۆکە دا ئەبەزێت...")

    output_template = f"video_{message.from_user.id}.mp4"

    ydl_opts = {
        'outtmpl': output_template,
        'format': 'best',
    }

    try:
        def download():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        await asyncio.to_thread(download)

        if os.path.exists(output_template):
            await message.answer_video(types.FSInputFile(output_template))
            os.remove(output_template)
            await bot.delete_message(chat_id=message.chat.id, message_id=processing_msg.message_id)
        else:
            await message.answer("❌ لێبوردە، نەمتوانی ڤیدیۆکە داببەزێنم. تکایە پشکنین بۆ لینکەکە بکە.")
            
    except Exception as e:
        await message.answer(f"❌ هەڵەیەک ڕوویدا: {str(e)}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
