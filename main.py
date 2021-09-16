import os
import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN')
matricula = os.getenv('MATRICULA')
password = os.getenv('SENHA')

bot = Bot('!')


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
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


@bot.command(name='freebsd')
async def send_hello(ctx):

    await ctx.send('Eu amo!')


bot.run(token)
