import discord
from discord.ext import commands
import yt_dlp
import asyncio

# Intents (İzinler) ayarı
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# yt-dlp Ayarları
YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'default_search': 'ytsearch',
    'source_address': '0.0.0.0'
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

@bot.event
async def on_ready():
    print(f'🔥 {bot.user.name} online! Feuer frei!')

@bot.command(name='cal', help='Rammstein şarkısı çalar. Örn: !cal Du Hast')
async def cal(ctx, *, sarki_adi: str):
    if not ctx.author.voice:
        await ctx.send("Önce bir ses kanalına girmelisin!")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client is None:
        vc = await channel.connect()
    else:
        vc = ctx.voice_client

    # Arama teriminin sonuna otomatik "Rammstein" ekliyoruz!
    arama_terimi = f"Rammstein {sarki_adi}"
    await ctx.send(f"🔍 **{sarki_adi}** Rammstein arşivinde aranıyor...")

    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(arama_terimi, download=False))

    if 'entries' in data:
        data = data['entries'][0]

    filename = data['url']
    baslik = data['title']

    if vc.is_playing():
        vc.stop()

    vc.play(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS))
    await ctx.send(f"🎸 Şimdi çalıyor: **{baslik}** 🤘")

@bot.command(name='dur', help='Müziği durdurur ve kanaldan ayrılır.')
async def dur(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Tschüss! Bot kanaldan ayrıldı.")
    else:
        await ctx.send("Zaten bir ses kanalında değilim.")

# BURAYA DİKKAT: Tırnak içine Discord Developer Portal'dan aldığın Token'ı yapıştıracaksın!
bot.run('MTU2NTYzMjA0NTM0MDgyNzcwOA.GOM9_9.Ub218UAqip2NUc_-KEczmeCRWljXHkEt-TrM7k')