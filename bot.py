from pyrogram import Client, filters, idle
import yt_dlp, asyncio, os

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("session", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

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
    if len(message.command) < 2:
        await message.reply("❌ اكتب اسم الفيلم\nمثال: /شغل اسم")
        return
    query = " ".join(message.command[1:])
    msg = await message.reply(f"🔍 جاري البحث: {query}")
    try:
        await msg.edit("⬇️ جاري التحميل...")
        video_file = download_video(query)
        await msg.edit(f"✅ تم تحميل: {query}\n\nأرسل الفيديو للمجموعة...")
        await app.send_video(message.chat.id, video_file, caption=f"🎬 {query}")
        os.remove(video_file)
    except Exception as e:
        await msg.edit(f"❌ خطأ: {str(e)}")

async def main():
    await app.start()
    print("✅ البوت يعمل!")
    await idle()

asyncio.run(main())
