import time
import datetime
from abilities_ids import ABILITIES_IDS
from heroes_data import hero_names

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


def get_time(): # [13.09.2022 - 14:54:34]
    now = datetime.datetime.now()
    return f'''[{now.day if now.day > 9 else '0' + str(now.day)}.{now.month if now.month > 9 else '0' + str(now.month)}.{now.year} - {now.hour if now.hour > 9 else '0' + str(now.hour)}:{now.minute if now.minute > 9 else '0' + str(now.minute)}:{now.second if now.second > 9 else '0' + str(now.second)}]'''


def hero_id_from_ability_id(ability_id):
    doubles = ['phantom', 'dark', 'shadow']
    ability = ABILITIES_IDS[ability_id].split('_')
    hero = ability[0]
    if hero in doubles:
        hero = f'{ability[0]}_{ability[1]}'
    hero_id = hero_names[hero]
    return hero_id