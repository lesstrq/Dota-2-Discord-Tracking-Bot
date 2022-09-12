from tokens import APP_ID, GUILD_ID, DISCORD_TOKEN, PUBLIC_KEY
import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

description = '''My test bot
idk im juss playin here
'''

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

bot.run(DISCORD_TOKEN)
