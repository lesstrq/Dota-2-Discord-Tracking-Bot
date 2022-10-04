import os

import requests
import getters
import discord
import emoji
import colors
import picture
import db_queries

OPENDOTA_API_URL = "https://api.opendota.com/api/"


def already_bound(dota_id):
    nickname = getters.get_nickname_by_dota_id(dota_id)
    embed = discord.Embed(title="Something went wrong!",
                          description=f"Your discord account is already bound to Dota 2 account named **{nickname}**\n"
                                      f"Use **?unbind** command if you want to unbind this account and bind a new one.",
                          color=colors.RED)
    return embed


def bound_successfully(discord_id, dota_id):
    player = getters.Player(dota_id)
    nickname = player.get_nickname()
    win, lose = player.get_wins(), player.get_loses()
    winrate = player.get_winrate()
    rank = player.get_rank() + player.get_leaderboard_rank()

    embed = discord.Embed(title="We're good!",
                          description=f"Successfully bound <@{discord_id}> to **{nickname}**",
                          color=0x7CFC00)
    embed.set_thumbnail(url=player.get_avatar_url())
    embed.add_field(name="W - L", value=f"{win} - {lose} ({winrate}%)", inline=True)
    embed.add_field(name="Rank", value=f"{rank}", inline=True)

    return embed


def closed_profile():
    embed = discord.Embed(title="Something went wrong!",
                          description="Make sure your match history is public and try again! \n "
                                      "To check if it is, go to "
                                      "*Settings* -> *Social* -> *Social* and look at the \n "
                                      "**Expose Public Match Data** option",
                          color=colors.RED)

    return embed


def unbind():
    embed = discord.Embed(title="Everything went smooth!",
                          description=f"Successfully unbound",
                          color=colors.GREEN)

    return embed


def recent(discord_id):
    dota_id = db_queries.get_dota_id(discord_id)

    if not dota_id:
        embed = discord.Embed(title="Something went wrong!",
                              description="Seems like you haven't bound your Dota 2 account!\n"
                                          "To do so, use the **?bind <id>** command.",
                              color=colors.RED)

        return [None, embed]

    game = getters.RecentGame(dota_id)

    player_info = requests.get(OPENDOTA_API_URL + f"players/{dota_id}").json()
    nickname = player_info["profile"]["personaname"]

    hero_name = game.get_hero_name()
    icon_url = game.get_hero_image_url()

    duration = game.get_duration()
    result = game.get_result()
    lobby_size = game.get_lobby_size()

    net_worth = game.get_net_worth()
    hero_damage = game.get_hero_damage()

    game_kda = game.get_kda()
    avg_kda = game.get_avg_kda()
    kda_emoji = emoji.choose_kda_emoji(game_kda, avg_kda)

    lobby_size_line = "**Played in** " \
                      + ("Solo Queue" if lobby_size == 1 or not lobby_size
                         else f"Party of {lobby_size}") + emoji.create_party_size_line(lobby_size)

    hero_line = f"Hero: **{hero_name}**"

    duration_line = f"Duration: **{duration['mins']}:{duration['secs']}**"

    result_line = f"Result: **{result} {emoji.win_or_lose_emoji(result)}**"

    kda_line = f"K/D/A: **{game.get_kills()}/{game.get_deaths()}/{game.get_assists()} {kda_emoji}**"

    net_worth_line = f"Net Worth: **{net_worth}**{emoji.MONEY_WITH_WINGS}"

    hero_damage_line = f"Hero Damage: **{hero_damage}**{emoji.CROSSED_SWORDS}"

    lines = [lobby_size_line,
             hero_line,
             duration_line,
             result_line,
             kda_line,
             net_worth_line,
             hero_damage_line]

    embed = discord.Embed(title=f"Last {nickname}'s match:",
                          description='\n'.join(lines),
                          color=(colors.RED if result == "Lose" else colors.GREEN))
    embed.set_thumbnail(url=icon_url)

    player = game.get_player_detailed_info()

    filename_inv = picture.create_image(player)
    file_inv = discord.File(filename_inv, filename="image.png")

    embed.set_image(url="attachment://image.png")

    return [file_inv, embed]
