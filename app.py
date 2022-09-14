from tokens import *
import discord
from discord.ext import commands
import psycopg2
import random
import requests
import json
import misc
from psycopg2.errors import UniqueViolation

OPENDOTA_API_URL = "https://api.opendota.com/api/"

insert_query = "INSERT INTO dota_track.discord_to_steam VALUES ({}, {})"


def connect():
    return psycopg2.connect(user=DATABASE_NAME,
                                  password=DATABASE_PASSWORD,
                                  host=DATABASE_SERVER,
                                  port=DATABASE_PORT,
                                  database=DATABASE_NAME)


try:
    connection = connect()
    pars = connection.get_dsn_parameters()
    print(f"{misc.get_time()} Successfully connected to DB {pars['dbname']} as user {pars['user']}")
    print(f"{misc.get_time()} Host: {pars['host']}")
    connection.close()

except Exception as e:
    print(e)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

description = '''
This is a bot that can show information about Dota 2 matches and players
'''

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def bind(ctx, dota_id):
    try:
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(f"SELECT dota_id FROM dota_track.discord_to_steam WHERE discord_id='{ctx.author.id}'")
        dota_id_in_db = cursor.fetchone()
        print(dota_id_in_db)
        if dota_id_in_db:
            player_info = requests.get(OPENDOTA_API_URL + f"players/{dota_id_in_db[0]}").json()
            nickname = player_info["profile"]["personaname"]
            embed = discord.Embed(title="Something went wrong!",
                                  description=f"Your discord account is already bound to Dota 2 account named **{nickname}**"
                                              f"+. \n Use **?unbind** command if you want to unbind this account and bind a new one.",
                                  color=0xff0000)
            await ctx.send(embed=embed)
            return
        print(f"{misc.get_time()} Executing {insert_query.format(ctx.author.id, dota_id)}")
        cursor.execute(insert_query.format(ctx.author.id, dota_id))
        connection.commit()
        print(f"{misc.get_time()} Inserted [{ctx.author.id}, {dota_id}] in dota_track.discord_to_steam")

        player_info = requests.get(OPENDOTA_API_URL + f"players/{dota_id}").json()
        nickname = player_info["profile"]["personaname"]
        win, lose = requests.get(OPENDOTA_API_URL + f"players/{dota_id}/wl").json().values()
        winrate = round(100 * win / (win + lose), 2)

        rank = misc.get_rank(player_info['rank_tier'])
        if player_info['leaderboard_rank']:
            rank += f"{player_info['leaderboard_rank']}"

        embed = discord.Embed(title="We're good!",
                              description=f"Successfully bound <@{ctx.author.id}> to **{nickname}**",
                              color=0x7CFC00)
        embed.set_thumbnail(url=player_info["profile"]["avatarfull"])
        embed.add_field(name="W - L", value=f"{win} - {lose} ({winrate}%)", inline=True)
        embed.add_field(name="Rank", value=f"{rank}", inline=True)

        connection.close()
        await ctx.send(embed=embed)
    except KeyError as ke:
        connection = connect()
        cursor = connection.cursor()
        print(f"{misc.get_time()} Someone with a closed profile tried to bind his account")
        delete_query = f"delete from dota_track.discord_to_steam where discord_id='{ctx.author.id}'"
        print(f"{misc.get_time()} Executing {delete_query}")
        cursor.execute(delete_query)
        connection.commit()
        embed = discord.Embed(title="Something went wrong!",
                              description="Make sure your match history is public and try again! \n To check if it is, go to *Settings* -> *Social* -> *Social* and look at the \n **Expose Public Match Data** option",
                              color=0xff0000)
        connection.close()
        await ctx.send(embed=embed)
    except UniqueViolation:
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(f"SELECT dota_id FROM dota_track.discord_to_steam WHERE discord_id='{ctx.author.id}'")
        dota_id = cursor.fetchall()
        player_info = requests.get(OPENDOTA_API_URL + f"players/{dota_id}").json()
        nickname = player_info["profile"]["personaname"]
        embed = discord.Embed(title="Something went wrong!",
                              description=f"Your discord account is already bound to Dota 2 account named {nickname}. \n Use **?unbind** command if you want to unbind this account and bind a new one.",
                              color=0xff0000)
        connection.close()
        await ctx.send(embed=embed)


@bot.command()
async def unbind(ctx):
    connection = connect()
    cursor = connection.cursor()
    delete_query = f"delete from dota_track.discord_to_steam where discord_id='{ctx.author.id}'"
    print(f"{misc.get_time()} Executing {delete_query}")
    cursor.execute(delete_query)
    connection.commit()
    embed = discord.Embed(title="Everything went smooth!",
                          description=f"Successfully unbound",
                          color=0x7CFC00)
    connection.close()
    await ctx.send(embed=embed)


@bot.command()
async def recent(ctx):
    connection = connect()
    cursor = connection.cursor()
    query = f"SELECT dota_id FROM dota_track.discord_to_steam WHERE discord_id='{ctx.author.id}'"
    cursor.execute(query)
    dota_id = cursor.fetchone()[0]
    game_info = requests.get(OPENDOTA_API_URL + f"players/{dota_id}/matches?limit=1").json()[0]
    player_info = requests.get(OPENDOTA_API_URL + f"players/{dota_id}").json()
    nickname = player_info["profile"]["personaname"]
    embed = discord.Embed(title=f"Last {nickname}'s match:",
                          description=f"Duration: {game_info['duration'] // 60}:{game_info['duration'] % 60}")
    await ctx.send(embed=embed)

bot.run(DISCORD_TOKEN)
