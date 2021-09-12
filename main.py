import discord
import os
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('Patrick'):
        await message.channel.send('Oi Pessoal! Espero encontrar vocês bem!')

token = os.getenv('TOKEN')
client.run(token)
