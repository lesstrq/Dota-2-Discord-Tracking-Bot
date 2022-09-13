from tokens import *
import discord
from discord.ext import commands
import psycopg2
import random
import requests
import json

OPENDOTA_API_URL = "https://api.opendota.com/api/"

def get_rank(n):
    rank_names = {
        1: "Herald",
        2: "Guardian",
        3: "Crusader",
        4: "Archon",
        5: "Legend",
        6: "Ancient",
        7: "Divine",
        8: "Immortal"
    }
    rank_stars = {
        0: "",
        1: "I",
        2: "II",
        3: "III",
        4: "IV",
        5: "V"
    }

    return f"{rank_names[n // 10]} {rank_stars[n % 10]}"

insert_query = "INSERT INTO dota_track.discord_to_steam VALUES ({}, {})"

try:
    connection = psycopg2.connect(user=DATABASE_NAME,
                                  password=DATABASE_PASSWORD,
                                  host=DATABASE_SERVER,
                                  port="5432",
                                  database=DATABASE_NAME)

    cursor = connection.cursor()
    schema_query = f'''
    CREATE SCHEMA IF NOT EXISTS dota_track
    AUTHORIZATION {DATABASE_NAME};
    '''
    cursor.execute(schema_query)
    connection.commit()
    print(connection.get_dsn_parameters())

except Exception as e:
    print(e)

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


@bot.command()
async def bind(ctx, dota_id):
    try:
        print(insert_query.format(ctx.author.id, dota_id))
        cursor.execute(insert_query.format(ctx.author.id, dota_id))
        connection.commit()
        player_info = requests.get(OPENDOTA_API_URL + f"players/{dota_id}").json()
        nickname = player_info["profile"]["personaname"]
        embed = discord.Embed(title="We're good!", description=f"Successfully bound <@{ctx.author.id}> to **{nickname}**", color=0x7CFC00)
        embed.set_thumbnail(url=player_info["profile"]["avatarfull"])
        win, lose = requests.get(OPENDOTA_API_URL + f"players/{dota_id}/wl").json().values()
        winrate = round(100 * win / (win + lose), 2)
        embed.add_field(name="W - L", value=f"{win} - {lose} ({winrate}%)", inline=True)
        rank = get_rank(player_info['rank_tier'])
        if player_info['leaderboard_rank']:
            rank += f"{player_info['leaderboard_rank']}"
        embed.add_field(name="MMR", value=f"Rank: {rank}", inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        print(e)
        embed = discord.Embed(title="Something went wrong!", description="Make sure your match history is open and try again!", color=0xff0000)
        await ctx.send(embed=embed)

bot.run(DISCORD_TOKEN)
