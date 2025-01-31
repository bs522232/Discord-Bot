import discord
from discord.ext import commands
import yt_dlp
import os

# FFmpeg 실행 파일 경로 직접 지정
FFMPEG_PATH = "C:/ffmpeg/bin/ffmpeg.exe"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Logged in as{bot.user}')

@bot.event
async def on_ready(): # 봇이 실행되면 한 번 실행됨
    print(f'Logged in as {bot.user}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("!명령어 사용 가능"))

@bot.event
async def on_message(message):
    if message.author.bot:  # 봇이 보낸 메시지는 무시
        return

    if message.content == "!명령어":
        embed = discord.Embed(colour=discord.Color.red(), title="명령어", description="아래 참고")
        embed.add_field(name="명령어.", value="!p URL 노래 재생.", inline=False)
        embed.add_field(name=" ", value="!s 또는 !stop 노래 중지.", inline=False)
        embed.add_field(name=" ", value="!j 또는 !join 음성채널 입장.", inline=False)
        embed.add_field(name=" ", value="!l 또는 !leave 음성채널 퇴장.", inline=False) #inline이 False라면 다음줄로 넘깁니다.
        await message.channel.send(embed=embed)

    await bot.process_commands(message)  # **이 줄 추가하면 명령어 정상 작동!**

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("!p URL을 사용하여 노래를 재생시켜 주세요.")
    else:
        await ctx.send("음성 채널에 먼저 접속해주세요!")

@bot.command()
async def j(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("!p URL을 사용하여 노래를 재생시켜 주세요.")
    else:
        await ctx.send("음성 채널에 먼저 접속해주세요!")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("봇이 음성 채널을 떠났습니다.")
    else:
        await ctx.send("봇이 음성 채널에 없습니다!")

@bot.command()
async def l(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("봇이 음성 채널을 떠났습니다.")
    else:
        await ctx.send("봇이 음성 채널에 없습니다!")

@bot.command()
async def play(ctx, url):
    if not ctx.voice_client:
        await ctx.invoke(join)
        await ctx.send("로딩중이니 잠시 기다려주세요.")
    ctx.voice_client.stop()

@bot.command()
async def p(ctx, url):
    if not ctx.voice_client:
        await ctx.invoke(join)
        await ctx.send("로딩중이니 잠시 기다려주세요.")
    ctx.voice_client.stop()
    
    FFMPEG_OPTIONS = {
    'executable': FFMPEG_PATH,
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

    YDL_OPTIONS = {'format': 'bestaudio'}
    
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        ctx.voice_client.play(source)

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
    else:
        await ctx.send("현재 재생 중인 노래가 없습니다!")

@bot.command()
async def s(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
    else:
        await ctx.send("현재 재생 중인 노래가 없습니다!")


access_token = os.environ["BOT_TOKEN"]
bot.run(access_token)
