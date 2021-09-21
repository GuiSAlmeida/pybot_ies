import os
import requests
import json
from datetime import datetime, timedelta
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


def create_embed(cls):
    embed = discord.Embed(
        title='Aula começando pessoal, não se atrasem!',
        description='Seguem dados para acesso ao link da aula.',
        color=0x065aa9,
    )
    embed.set_author(
        name=bot.user.name,
        icon_url=bot.user.avatar_url
    )
    embed.add_field(name='Disciplina', value=cls['NomeDisciplina'])
    embed.add_field(name='Professor', value=cls['Professor'])

    if cls['Link']:
        embed.add_field(name='Link', value=cls['Link'], inline=False)

    embed.set_thumbnail(url='https://www.ies.edu.br/assets/img/logo.png')
    embed.set_footer(
        text='Para mais infos das aulas acesse: https://www.ies.edu.br/')

    return embed


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    # current_time.start()
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


@bot.command(name='aulas')
async def send_embed(ctx):
    now = datetime.now()
    print(now)
    now_date = now.strftime('%Y-%m-%d')

    """ Login na api para pegar token """
    url_login = f'https://www.ies.edu.br/includes/head.asp' \
        f'?action=logar&matricula={matricula}&senha={password}'

    login = requests.get(url_login)
    data_login = json.loads(login.text)
    user_token = data_login['token']

    """ Bate na api para pegar dados das aulas """
    url_classes = f'https://suafaculdade.com.br' \
        f'/api/servicos/Aluno/ObterAulaOnline/{user_token}'

    data_classes = requests.get(url_classes)
    classes = json.loads(data_classes.text)

    for cls in classes:
        if now_date in cls['DataAula']:
            embed = create_embed(cls)
            await ctx.send(embed=embed)


# @tasks.loop(minutes=1)
# async def current_time():
#     channel = bot.get_channel(889644549192974336)

#     now = datetime.now() - timedelta(minutes=3*60)
#     print(now)
#     now_time = now.strftime('%H:%M:00')
#     now_date = now.strftime('%Y-%m-%d')

#     if '19:30:00' in now_time or '20:45:00' in now_time:

#         """ Login na api para pegar token """
#         url_login = f'https://www.ies.edu.br/includes/head.asp' \
#             f'?action=logar&matricula={matricula}&senha={password}'

#         login = requests.get(url_login)
#         data_login = json.loads(login.text)
#         user_token = data_login['token']

#         """ Bate na api para pegar dados das aulas """
#         url_classes = f'https://suafaculdade.com.br' \
#             f'/api/servicos/Aluno/ObterAulaOnline/{user_token}'

#         data_classes = requests.get(url_classes)
#         classes = json.loads(data_classes.text)

#         for cls in classes:
#             if not isinstance(cls, dict):
#                 cls = json.dumps(cls)

#             if now_date in cls['DataAula'] and '19:30:00' in cls['DataAula']:
#                 embed = create_embed(cls)
#                 await channel.send(embed=embed)


bot.run(token)
