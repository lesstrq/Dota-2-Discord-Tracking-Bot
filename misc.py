import datetime
from constants.ability_ids import ABILITIES_IDS
from heroes_data import hero_names
import os


def get_rank(rank_number: int) -> str:
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

    return f"{rank_names[rank_number // 10]} {rank_stars[rank_number % 10]}"


def get_time() -> str:  # [13.09.2022 - 14:54:34]
    now = datetime.datetime.now()
    return f"[{now.day if now.day > 9 else '0' + str(now.day)}." \
           f"{now.month if now.month > 9 else '0' + str(now.month)}." \
           f"{now.year} - {now.hour if now.hour > 9 else '0' + str(now.hour)}" \
           f":{now.minute if now.minute > 9 else '0' + str(now.minute)}:" \
           f"{now.second if now.second > 9 else '0' + str(now.second)}]"


def hero_id_from_ability_id(ability_id: str) -> int:
    doubles = ['phantom', 'dark', 'shadow']
    ability = ABILITIES_IDS[ability_id].split('_')
    hero = ability[0]
    if hero in doubles:
        hero = f'{ability[0]}_{ability[1]}'
    hero_id = hero_names[hero]
    return hero_id


def clear_temp():
    directory = "temporary_pictures/"
    for file in os.listdir(directory):
        os.remove(os.path.join(directory, file))


def convert_unix_to_readable(unix_time, utc=3):
    return datetime.datetime.utcfromtimestamp(unix_time + utc * 3600).strftime('%H:%M on %d %B of %Y') \
           + f" (UTC {'+' if utc >= 0 else ''}{utc})"


def is_win(player_slot, radiant_win):
    if radiant_win:
        if player_slot < 100:
            return True
        return False
    else:
        if player_slot < 100:
            return False
        return True
