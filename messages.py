import requests
import getters
import discord
import emoji
import colors
import picture
from database import db_queries
from getters import PlayerNotInGameException

OPENDOTA_API_URL = "https://api.opendota.com/api/"


def dota_id_is_not_digit():
    embed = discord.Embed(title="Wrong ID format!",
                          description="Dota 2 player ID should be digit",
                          color=colors.RED)

    return embed


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


def wrong_id():
    embed = discord.Embed(title="Something went wrong!",
                          description="Dota 2 player ID is wrong or their match history is private!",
                          color=colors.RED)

    return embed


def player_not_in_game(game_id):
    embed = discord.Embed(title="Something went wrong!",
                          description=f"This player didn't take part in game №{game_id}",
                          color=colors.RED)

    return embed


def unbind():
    embed = discord.Embed(title="Everything went smooth!",
                          description=f"Successfully unbound",
                          color=colors.GREEN)

    return embed


def stats(discord_id=None, dota_id=None):
    if not dota_id:
        dota_id = db_queries.get_dota_id(discord_id)
    player = getters.Player(dota_id)

    rank = player.get_rank()
    last_days_games, last_days_wins, last_days_loses, last_days_winrate = player.get_stats_for_last_n_days().values()

    most_played_heroes_data = player.get_most_played_heroes()

    empty_line = ''

    rank_line = f"**Rank:** {rank}"

    last_days_line = f"**Last 30 days stats:** \nGames played: " \
                     f"{last_days_games}\nWinrate: {last_days_wins} - {last_days_loses} ({last_days_winrate}%)"

    hero_lines = ['**Most played heroes:**']
    for hero in most_played_heroes_data:
        hero_line = f"**{hero['hero_name']}:** {hero['games']} games played | " \
                    f"{hero['wins']} - {hero['loses']} ({hero['winrate']}%)"
        hero_lines.append(hero_line)

    lines = [rank_line,
             empty_line,
             last_days_line,
             empty_line] + hero_lines

    embed = discord.Embed(title=f"{player.get_nickname()}'s stats:",
                          description='\n'.join(lines))
    embed.set_thumbnail(url=player.get_avatar_url())

    return embed


def recent(discord_id=None, dota_id=None, game_id=None):
    if not dota_id:
        dota_id = db_queries.get_dota_id(discord_id)

    if not dota_id:
        embed = discord.Embed(title="Something went wrong!",
                              description="Seems like you haven't bound your Dota 2 account!\n"
                                          "To do so, use the **?bind <id>** command.",
                              color=colors.RED)

        return [None, embed]
    try:
        if game_id:
            game = getters.Game(dota_id, int(game_id))
        else:
            game = getters.RecentGame(dota_id)
    except KeyError:
        return [None, wrong_id()]
    except IndexError:
        return [None, wrong_id()]
    except PlayerNotInGameException:
        return [None, player_not_in_game(game_id)]

    player_info = requests.get(OPENDOTA_API_URL + f"players/{dota_id}").json()
    nickname = player_info["profile"]["personaname"]

    hero_name = game.get_hero_name()
    icon_url = game.get_hero_image_url()

    duration = game.get_duration()
    result = game.get_result()
    lobby_size = game.get_lobby_size()

    net_worth = game.get_net_worth()
    gold_per_minute = game.get_gold_per_minute()
    xp_per_minute = game.get_xp_per_minute()

    last_hits = game.get_last_hits()
    denies = game.get_denies()

    hero_damage = game.get_hero_damage()
    tower_damage = game.get_tower_damage()

    hero_healing = game.get_hero_healing()

    game_kda = game.get_kda()
    avg_kda = game.get_avg_kda()
    kda_emoji = emoji.choose_kda_emoji(game_kda, avg_kda)

    overall_wins, overall_loses, overall_winrate = game.get_played_hero_stats()
    last20_wins, last20_loses, last20_winrate = game.get_played_hero_stats_last_20_games()

    empty_line = "\n"

    start_time_line = f"{emoji.CLOCK} **{game.get_game_start_time()}**"

    lobby_size_line = "**Played in** " \
                      + ("Solo Queue" if lobby_size == 1 or not lobby_size
                         else f"Party of {lobby_size}") + emoji.create_party_size_line(lobby_size)

    hero_line = f"Hero: **{hero_name}**"

    duration_line = f"Duration: **{duration['mins']}:{duration['secs']}**"

    result_line = f"Result: **{result} {emoji.win_or_lose_emoji(result)}**"

    kda_line = f"{kda_emoji}K/D/A: **{game.get_kills()}/{game.get_deaths()}/{game.get_assists()}" \
               f"{emoji.top_emoji(game.get_top_kda(), game_kda)}**"

    net_worth_line = f"{emoji.MONEY_WITH_WINGS}Net Worth: " \
                     f"**{net_worth}**{emoji.top_emoji(game.get_top_net_worth(), net_worth)}"

    benchmarks_line = f"{emoji.SCALES}GPM: **{gold_per_minute}**   XPM: **{xp_per_minute}**"

    lh_dn_line = f"LH/DN : **{last_hits}/{denies}**" \
                 f"{emoji.top_emoji(game.get_top_last_hits(), last_hits)}"

    hero_damage_line = f"{emoji.CROSSED_SWORDS}Hero Damage: **{hero_damage}**" \
                       f"{emoji.top_emoji(game.get_top_hero_damage(), hero_damage)}"
    tower_damage_line = f"{emoji.HAMMER}Tower Damage: **{tower_damage}" \
                        f"{emoji.top_emoji(game.get_top_tower_damage(), tower_damage)}**"

    hero_healing_line = f"{emoji.MENDING_HEART}Hero Healing: **{hero_healing}" \
                        f"{emoji.top_emoji(game.get_top_hero_healing(), hero_healing)}**"

    overall_hero_stats_line = f"Overall **{hero_name}** winrate: " \
                              f"**{overall_wins} - {overall_loses} ({overall_winrate}%**)"

    last20_stats_line = f"**{hero_name}** winrate in last 20 matches: " \
                              f"**{last20_wins} - {last20_loses} ({last20_winrate}%**)"

    lines = [start_time_line,
             lobby_size_line,
             empty_line,
             hero_line,
             duration_line,
             result_line,
             empty_line,
             kda_line,
             net_worth_line,
             benchmarks_line,
             lh_dn_line,
             empty_line,
             hero_damage_line,
             tower_damage_line,
             hero_healing_line,
             empty_line,
             overall_hero_stats_line,
             last20_stats_line]

    title = f"Last {nickname}'s match:" if not game_id else f"{nickname}'s performance \nin match №{game_id}"

    embed = discord.Embed(title=title,
                          description='\n'.join(lines),
                          color=(colors.RED if result == "Lose" else colors.GREEN))

    embed.set_thumbnail(url=icon_url)

    player = game.get_player_detailed_info()

    filename_inv = picture.create_image(player)
    file_inv = discord.File(filename_inv, filename="image.png")

    embed.set_image(url="attachment://image.png")

    return [file_inv, embed]
