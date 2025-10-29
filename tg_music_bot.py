import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import yt_dlp
import tempfile
import subprocess

BOT_TOKEN = os.getenv("TG_BOT_TOKEN")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message.video and not message.document:
        return

    file = message.video or message.document
    file_path = await file.get_file()
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        await file_path.download_to_drive(tmp.name)
        video_path = tmp.name

    audio_path = video_path.replace(".mp4", ".mp3")

    subprocess.run(["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path])

    await message.reply_audio(audio=open(audio_path, "rb"), caption="🎧 اینم صدای ویدیوت!")

    os.remove(video_path)
    os.remove(audio_path)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))

if __name__ == "__main__":
    print("✅ Bot is running...")
    app.run_polling()
