from pyrogram import Client, filters
from pytube import YouTube
import os

# ==========================
#   BOT CONFIGURATION
# ==========================
API_ID = 33133552 # ← Replace with your API ID
API_HASH = "909bad054789f8491fb358753ab8ae55"  # ← Replace with your API HASH
BOT_TOKEN = "8577123802:AAFIRMoZLh-7ttOyR1aHOGhV52JGl-Sc6_M"  # ← Replace with your BOT TOKEN

app = Client(
    "music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ==========================
#   START COMMAND
# ==========================
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "**🎵 Welcome to Music Downloader Bot!**\n"
        "Send me a *YouTube link*, and I will give you the song as an audio file."
    )

# ==========================
#   DOWNLOAD SONG HANDLER
# ==========================
@app.on_message(filters.text & ~filters.command("start"))
async def download_song(client, message):

    url = message.text

    if "youtube.com" not in url and "youtu.be" not in url:
        await message.reply("❌ Please send a valid YouTube link.")
        return

    m = await message.reply("⏳ Downloading... Please wait.")

    try:
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()

        file_path = audio.download()

        # Rename to .mp3
        new_file = file_path.replace(".mp4", ".mp3")
        os.rename(file_path, new_file)

        await m.edit("🎶 Uploading your song...")

        # Send audio
        await message.reply_audio(
            audio=new_file,
            title=yt.title,
            performer="YouTube",
        )

        # Delete local file
        os.remove(new_file)

        await m.delete()

    except Exception as e:
        await m.edit(f"❌ Error: {e}")

# ==========================
#   START BOT
# ==========================
app.run()
