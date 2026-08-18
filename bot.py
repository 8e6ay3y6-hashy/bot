import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
import yt_dlp

# تۆکەنی بۆتەکەت لێرە دابنێ
TOKEN = "YOUR_BOT_TOKEN"

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "سڵاو! 👋\n"
        "من بۆتی دابەزاندنی ڤیدیۆم.\n"
        "لینکێکی تیکتۆک، ئینستاگرام یان یوتیۆمم بۆ بنێرە تا بۆت دابەزێنم!"
    )

@dp.message(F.text.startswith("http"))
async def download_video(message: types.Message):
    url = message.text.strip()
    processing_msg = await message.answer("⏳ خەریکی دابەزاندنی ڤیدیۆکەم، تکایە چاوەڕوان ببن...")

    output_template = f"video_{message.from_user.id}.mp4"

    ydl_opts = {
        'format': 'best',
        'outtmpl': output_template,
        'max_filesize': 50 * 1024 * 1024,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if os.path.exists(output_template):
            video_file = types.FSInputFile(output_template)
            await message.answer_video(video=video_file, caption="✅ فەرموون ڤیدیۆکەت!")
            await bot.delete_message(chat_id=message.chat.id, message_id=processing_msg.message_id)
            os.remove(output_template)
        else:
            await processing_msg.edit_text("❌ لێبووردن، ناتوانم ئەم ڤیدیۆیە دابەزێنم.")

    except Exception as e:
        logging.error(f"Error: {e}")
        await processing_msg.edit_text("❌ هەڵەیەک ڕوویدا. دڵنیابە لەوەی لینکەکە ڕاستە و قەبارەکەی زۆر گەورە نییە.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
