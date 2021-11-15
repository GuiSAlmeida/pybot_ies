import os
from utils import get_classes, create_embed
from datetime import datetime, timedelta
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN')
bot = commands.Bot('!')


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

    current_time.start()

    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.Game('Assembly no FreeBSD')
    )


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if 'Patrick' in message.content:
        await message.channel.send(f'Oi {message.author.name}, olá pessoal '
                                   f'espero encontrar vocês bem!')

    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(877701880472547328)
    embed = discord.Embed(
        title='Bem vindo!',
        description=f'{member.name} entrou pra turma da IES.',
        color=0x065aa9,
    )
    embed.set_author(
        name=bot.user.name,
        icon_url=bot.user.avatar_url
    )
    embed.set_thumbnail(url=member.avatar_url)

    await channel.send(embed=embed)


@bot.command(name='freebsd')
async def send_hello(ctx):
    await ctx.send('Eu amo!')


@tasks.loop(minutes=1)
async def current_time():
    channel = bot.get_channel(889644549192974336)

    """
    Timedelta subtract 3 hours from current time
    because heroku server is from another time zone.
    """
    now = datetime.now() - timedelta(minutes=3*60)

    now_time = now.strftime('%H:%M:00')
    now_date = now.strftime('%Y-%m-%d')

    if '19:10:00' in now_time or '20:45:00' in now_time:
        classes = get_classes()

        for cls in classes:
            if now_date in cls['DataAula'] and now_time in cls['DataAula']:
                embed = create_embed(cls, bot)
                await channel.send(embed=embed)


bot.run(token)
