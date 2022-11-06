import asyncio

import messages
from tokens import *
import discord
from discord.ext import commands
from discord import app_commands
from database.db_connection import check_connection
import misc
from database import db_queries


try:
    check_connection()

except Exception as e:
    print(f"Unable to reach database. The following error has occurred: {e}")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

description = '''
This is a bot that can show information about Dota 2 matches and players
'''

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")


@tree.command()
async def bind(interaction, dota_id: str):
    try:
        dota_id_in_db = db_queries.get_dota_id(interaction.user.id)
        if dota_id_in_db:
            await interaction.response.send_message(embed=messages.already_bound(dota_id_in_db))
            return

        if not dota_id.isdigit():
            await interaction.response.send_message(embed=messages.dota_id_is_not_digit())
            return

        db_queries.insert_dota_id(interaction.user.id, dota_id)
        await interaction.response.send_message(embed=messages.bound_successfully(interaction.user.id, dota_id))

    except KeyError:
        db_queries.delete_record(interaction.user.id)
        await interaction.response.send_message(embed=messages.closed_profile())


@tree.command()
async def unbind(interaction):
    db_queries.delete_record(interaction.user.id)
    await interaction.response.send_message(embed=messages.unbind())


@tree.command(name="recent", description="Shows your last game stats")
async def recent(interaction, some_id: str = None):
    misc.clear_temp()
    await interaction.response.defer()
    if some_id:
        if '@' in some_id:
            file_inv, embed = messages.recent(some_id[2:-1])
        else:
            file_inv, embed = messages.recent(dota_id=some_id)

    else:
        file_inv, embed = messages.recent(interaction.user.id)
    await interaction.followup.send(file=file_inv, embed=embed)


@tree.command(name="game",
              description="Shows your performance in game with given id",
              guild=discord.Object(id=714499919137865808))
async def game(interaction, game_id: str, discord_id: str = None):
    misc.clear_temp()
    await interaction.response.defer()
    print(discord_id, interaction.user.id)
    if discord_id:
        file_inv, embed = messages.recent(discord_id[2:-1], game_id=game_id)
    else:
        file_inv, embed = messages.recent(discord_id=interaction.user.id, game_id=game_id)
    await interaction.followup.send(file=file_inv, embed=embed)


@tree.command()
async def stats(interaction, some_id: str = None):
    await interaction.response.defer()
    if some_id:
        if '@' in some_id:
            embed = messages.stats(some_id[2:-1])
        else:
            embed = messages.stats(dota_id=some_id)
    else:
        embed = messages.stats(interaction.user.id)
    await interaction.followup.send(embed=embed)


@tree.command(name="test", description="Test Description Text")
async def first_command(interaction):
    await interaction.response.send_message("Hello!")


client.run(DISCORD_TOKEN)
