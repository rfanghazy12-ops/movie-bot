from pyrogram import Client, filters, idle
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputAudioVideoPiped
import yt_dlp, asyncio, os

API_ID = int(os.environ.get("35797401"))
API_HASH = os.environ.get("6c23b4fee5bd582a4cfe1e254509ffe2")
BOT_TOKEN = os.environ.get("8679055344:AAHp8ACyh3uE6wqASLdqbYbGsqnmvWi-s6E")

app = Client("session", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
pytgcalls = PyTgCalls(app)

def download_video(query):
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'movie.%(ext)s',
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        url = query if query.startswith("http") else f"ytsearch1:{query}"
        info = ydl.extract_info(url, download=True)
        if 'entries' in info:
            info = info['entries'][0]
        return ydl.prepare_filename(info)

@app.on_message(filters.command("شغل") & filters.group)
async def play_movie(client, message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        await message.reply("❌ اكتب اسم الفيلم\nمثال: /شغل اسم")
        return
    query = " ".join(message.command[1:])
    msg = await message.reply(f"🔍 جاري البحث: {query}")
    try:
        await msg.edit("⬇️ جاري التحميل...")
        video_file = download_video(query)
        await msg.edit("🎬 جاري البدء...")
        await pytgcalls.join_group_call(chat_id, InputAudioVideoPiped(video_file))
        await msg.edit(f"▶️ يتم عرض: {query}\n\nلإيقاف: /وقف")
    except Exception as e:
        await msg.edit(f"❌ خطأ: {str(e)}")

@app.on_message(filters.command("وقف") & filters.group)
async def stop_movie(client, message):
    try:
        await pytgcalls.leave_group_call(message.chat.id)
        await message.reply("⏹ تم الإيقاف")
    except Exception as e:
        await message.reply(f"❌ {str(e)}")

@app.on_message(filters.command("بوز") & filters.group)
async def pause_movie(client, message):
    try:
        await pytgcalls.pause_stream(message.chat.id)
        await message.reply("⏸ إيقاف مؤقت")
    except Exception as e:
        await message.reply(f"❌ {str(e)}")

@app.on_message(filters.command("استمر") & filters.group)
async def resume_movie(client, message):
    try:
        await pytgcalls.resume_stream(message.chat.id)
        await message.reply("▶️ استمر العرض")
    except Exception as e:
        await message.reply(f"❌ {str(e)}")

async def main():
    await pytgcalls.start()
    print("✅ البوت يعمل!")
    await idle()

asyncio.run(main())
