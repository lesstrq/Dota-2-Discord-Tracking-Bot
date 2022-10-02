from tokens import *
import discord
from discord.ext import commands
import psycopg2
import random
import requests
import json
import misc
from psycopg2.errors import UniqueViolation
import picture
import os

OPENDOTA_API_URL = "https://api.opendota.com/api/"

player_slots = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 128: 5, 129: 6, 130: 7, 131: 8, 132: 9}


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
async def recent(ctx, amount=1):
    connection = connect()
    cursor = connection.cursor()
    query = f"SELECT dota_id FROM dota_track.discord_to_steam WHERE discord_id='{ctx.author.id}'"
    cursor.execute(query)
    dota_id = cursor.fetchone()[0]
    games_info = requests.get(OPENDOTA_API_URL + f"players/{dota_id}/matches?limit={amount}").json()
    for game_info in games_info:
        detailed_game_info = requests.get(f"http://api.opendota.com/api/matches/{game_info['match_id']}").json()
        player_info = requests.get(OPENDOTA_API_URL + f"players/{dota_id}").json()
        nickname = player_info["profile"]["personaname"]
        cursor.execute(
            f"SELECT localized_name, scoreboard_icon_url FROM dota_track.heroes_data WHERE hero_id={game_info['hero_id']}")
        hero = cursor.fetchone()
        hero_name = hero[0]
        icon_url = hero[1]
        all_games_info = requests.get(OPENDOTA_API_URL + f'players/{dota_id}/matches?hero_id={game_info["hero_id"]}').json()
        kills, deaths, assists = 0, 0, 0
        for match in all_games_info:
            print(match)
            kills += match["kills"]
            deaths += match["deaths"]
            assists += match["assists"]
        avg_kda = (kills + assists) / deaths

        duration = {'mins': game_info['duration'] // 60,
                    'secs': ("0" if game_info['duration'] % 60 < 10 else "") + str(game_info['duration'] % 60)}
        result = "Win" if (game_info['player_slot'] > 100 and not game_info['radiant_win']) or (game_info['player_slot'] < 100 and game_info['radiant_win']) else "Lose"
        queue = "**Played in** " + ("Solo Queue" if game_info['party_size'] == 1 or not game_info['party_size'] else f"Party of {game_info['party_size']}") + (":bust_in_silhouette:" * game_info['party_size'])
        player_slot = game_info['player_slot']
        net_worth = detailed_game_info['players'][player_slots[player_slot]]['net_worth']
        hero_damage = detailed_game_info['players'][player_slots[player_slot]]['hero_damage']
        game_kda = (game_info['kills'] + game_info['assists']) / game_info['deaths']
        kda_emoji = ""
        if game_kda >= avg_kda:
            kda_emoji = ":arrow_up_small:"
        if game_kda < avg_kda:
            kda_emoji = ":arrow_down_small:"
        if game_kda > avg_kda * 2:
            kda_emoji = ":arrow_double_up:"
        if game_kda < avg_kda / 2:
            kda_emoji = ":arrow_double_down:"
        embed = discord.Embed(title=f"Last {nickname}'s match:",
                              description=f"{queue}\n"
                                          f"Hero: **{hero_name}**\n"
                                          f"Duration: **{duration['mins']}:{duration['secs']}**\n"
                                          f"Result: **{result} {':white_check_mark:' if result == 'Win' else ':x:'}**\n"
                                          f"K/D/A: **{game_info['kills']}/{game_info['deaths']}/{game_info['assists']} {kda_emoji}**\n"
                                          f"Net Worth: **{net_worth}**:money_with_wings:\n"
                                          f"Hero Damage: **{hero_damage}**:crossed_swords:",
                              color=(0xff0000 if result == "Lose" else 0x7cfc00))
        embed.set_thumbnail(url=icon_url)

        players = detailed_game_info['players']
        items = {}
        for player in players:
            if str(player['account_id']) == dota_id:
                for slot in picture.slots:
                    items[slot] = player[slot]
                skill_build = player['ability_upgrades_arr']
                level = player['level']

        filename_inv = picture.create_image(items)
        filename_skill = picture.create_skill_build_image(skill_build, level)
        file_inv = discord.File(filename_inv, filename="image.png")
        file_skill = discord.File(filename_skill, filename="image1.png")
        embed.set_image(url="attachment://image.png")
        files = [file_inv, file_skill]
        await ctx.send(file=file_inv, embed=embed)
        embed = discord.Embed(title='Skill Build:', color=(0xff0000 if result == "Lose" else 0x7cfc00))
        embed.set_image(url="attachment://image1.png")
        await ctx.send(file=file_skill, embed=embed)
        os.remove(filename_inv)
        os.remove(filename_skill)

bot.run(DISCORD_TOKEN)
