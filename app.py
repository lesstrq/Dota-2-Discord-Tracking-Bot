import messages
from tokens import *
import discord
from discord.ext import commands
from db_connection import check_connection
import misc
import os
import db_queries


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

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('--------------------------------------------')


@bot.command()
async def bind(ctx, dota_id):
    try:
        dota_id_in_db = db_queries.get_dota_id(ctx.author.id)
        if dota_id_in_db:
            await ctx.send(embed=messages.already_bound(dota_id_in_db))
            return

        db_queries.insert_dota_id(ctx.author.id, dota_id)
        await ctx.send(embed=messages.bound_successfully(ctx.author.id, dota_id))

    except KeyError:
        db_queries.delete_record(ctx.author.id)
        await ctx.send(embed=messages.closed_profile())


@bot.command()
async def unbind(ctx):
    db_queries.delete_record(ctx.author.id)
    await ctx.send(embed=messages.unbind())


@bot.command()
async def recent(ctx):
    file_inv, embed = messages.recent(ctx.author.id)
    await ctx.send(file=file_inv, embed=embed)
    misc.clear_temp()

bot.run(DISCORD_TOKEN)
