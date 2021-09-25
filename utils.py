import os
import requests
import json
import discord
from dotenv import load_dotenv

load_dotenv()

matricula = os.getenv('MATRICULA')
password = os.getenv('SENHA')


def get_classes():
    url_login = f'https://www.ies.edu.br/includes/head.asp' \
        f'?action=logar&matricula={matricula}&senha={password}'

    login = requests.get(url_login)
    data_login = json.loads(login.text)
    user_token = data_login['token']
    print(user_token)

    url_classes = f'https://suafaculdade.com.br' \
        f'/api/servicos/Aluno/ObterAulaOnline/{user_token}'

    data_classes = requests.get(url_classes)
    print(data_classes)
    classes = json.loads(data_classes.text)

    return classes


def create_embed(cls, bot):
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
