import os
import requests
import json
from datetime import datetime
from locale import setlocale, LC_TIME

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

setlocale(LC_TIME, 'pt_BR.UTF-8')
load_dotenv()

token = os.getenv('TOKEN')
matricula = os.getenv('MATRICULA')
password = os.getenv('SENHA')

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


@bot.command(name='freebsd')
async def send_hello(ctx):

    await ctx.send('Eu amo!')


@tasks.loop(minutes=1)
async def current_time():
    channel = bot.get_channel(877689818094633070)

    now = datetime.now()
    print(now)
    now_time = now.strftime('%H:%M:00')
    now_date = now.strftime('%Y-%m-%d')

    if '22:10:00' in now_time or '23:45:00' in now_time:

        # Login na api para pegar token
        url_login = f'https://www.ies.edu.br/includes/head.asp' \
            f'?action=logar&matricula={matricula}&senha={password}'

        login = requests.get(url_login)
        data_login = json.loads(login.text)
        user_token = data_login['token']

        # Bate na api para pegar dados das aulas
        url_classes = f'https://suafaculdade.com.br' \
            f'/api/servicos/Aluno/ObterAulaOnline/{user_token}'

        data_classes = requests.get(url_classes)
        classes = json.loads(data_classes.text)

        for cls in classes:
            if now_date in cls['DataAula'] and now_time in cls['DataAula']:
                await channel.send(json.dumps(cls, sort_keys=False, indent=4))


bot.run(token)
