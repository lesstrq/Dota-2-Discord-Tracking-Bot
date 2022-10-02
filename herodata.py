import psycopg2
import requests
from tokens import *

OPENDOTA_API_URL = "https://api.opendota.com/api/"

heroes = requests.get(OPENDOTA_API_URL + "heroes").json()

connection = psycopg2.connect(user=DATABASE_NAME,
                                  password=DATABASE_PASSWORD,
                                  host=DATABASE_SERVER,
                                  port=DATABASE_PORT,
                                  database=DATABASE_NAME)
cursor = connection.cursor()

# for hero in heroes:
#     hero_id = hero['id']
#     name = hero['name']
#     localized_name = hero['localized_name']
#     if "'" in localized_name:
#         temp = localized_name.split("'")
#         print(temp)
#         localized_name = temp[0] + "''" + temp[1]
#     cursor.execute(f"INSERT INTO dota_track.heroes_data (hero_id, name, localized_name) VALUES ({hero_id}, '{name}', '{localized_name}')")



HERO_ID_TO_PIC_URL = {
    "Anti-Mage": "https://static.wikia.nocookie.net/dota2_gamepedia/images/8/8e/Anti-Mage_icon.png/revision/latest/scale-to-width-down/120?cb=20200916215957",
    "Axe": "https://static.wikia.nocookie.net/dota2_gamepedia/images/2/23/Axe_icon.png/revision/latest/scale-to-width-down/120?cb=20160411211422",
    "Abaddon": "https://static.wikia.nocookie.net/dota2_gamepedia/images/2/26/Abaddon_icon.png/revision/latest/scale-to-width-down/120?cb=20210125060638",
    "Alchemist": "https://static.wikia.nocookie.net/dota2_gamepedia/images/f/fe/Alchemist_icon.png/revision/latest/scale-to-width-down/120?cb=20160411210240",
    "Ancient Apparition": "https://static.wikia.nocookie.net/dota2_gamepedia/images/6/67/Ancient_Apparition_icon.png/revision/latest/scale-to-width-down/120?cb=20160411220816",
    "Arc Warden": "https://static.wikia.nocookie.net/dota2_gamepedia/images/0/07/Arc_Warden_icon.png/revision/latest/scale-to-width-down/120?cb=20160411214723",
    "Bane": "https://static.wikia.nocookie.net/dota2_gamepedia/images/c/c3/Bane_icon.png/revision/latest/scale-to-width-down/120?cb=20160411215925",
    "Batrider": "https://static.wikia.nocookie.net/dota2_gamepedia/images/f/f2/Batrider_icon.png/revision/latest/scale-to-width-down/120?cb=20160411220708",
    "Beastmaster": "https://static.wikia.nocookie.net/dota2_gamepedia/images/d/d9/Beastmaster_icon.png/revision/latest/scale-to-width-down/120?cb=20160411205834",
    "Bloodseeker": "https://static.wikia.nocookie.net/dota2_gamepedia/images/5/56/Bloodseeker_icon.png/revision/latest/scale-to-width-down/120?cb=20160411213712",
    "Bounty Hunter": "https://static.wikia.nocookie.net/dota2_gamepedia/images/a/a6/Bounty_Hunter_icon.png/revision/latest/scale-to-width-down/120?cb=20160411213244",
    "Brewmaster": "https://static.wikia.nocookie.net/dota2_gamepedia/images/1/1e/Brewmaster_icon.png/revision/latest/scale-to-width-down/120?cb=20160411210333",
    "Bristleback": "https://static.wikia.nocookie.net/dota2_gamepedia/images/4/4d/Bristleback_icon.png/revision/latest/scale-to-width-down/120?cb=20160411210744",
    "Broodmother": "https://static.wikia.nocookie.net/dota2_gamepedia/images/d/df/Broodmother_icon.png/revision/latest/scale-to-width-down/120?cb=20160411214142",
    "Centaur Warrunner": "https://static.wikia.nocookie.net/dota2_gamepedia/images/e/ed/Centaur_Warrunner_icon.png/revision/latest/scale-to-width-down/120?cb=20160411210603",
    "Chaos Knight": "https://static.wikia.nocookie.net/dota2_gamepedia/images/f/fe/Chaos_Knight_icon.png/revision/latest/scale-to-width-down/120?cb=20160411212259",
    "Chen": "https://static.wikia.nocookie.net/dota2_gamepedia/images/6/61/Chen_icon.png/revision/latest/scale-to-width-down/120?cb=20160411215432",
    "Clinkz": "https://static.wikia.nocookie.net/dota2_gamepedia/images/c/cb/Clinkz_icon.png/revision/latest/scale-to-width-down/120?cb=20160411214114",
    "Clockwerk": "https://static.wikia.nocookie.net/dota2_gamepedia/images/d/d8/Clockwerk_icon.png/revision/latest/scale-to-width-down/120?cb=20160411210004",
    "Crystal Maiden": "https://static.wikia.nocookie.net/dota2_gamepedia/images/2/27/Crystal_Maiden_icon.png/revision/latest/scale-to-width-down/120?cb=20160411214805",
    "Dark Seer": "https://static.wikia.nocookie.net/dota2_gamepedia/images/c/c5/Dark_Seer_icon.png/revision/latest/scale-to-width-down/120?cb=20160411220632",
    "Dark Willow": "https://static.wikia.nocookie.net/dota2_gamepedia/images/3/3c/Dark_Willow_icon.png/revision/latest/scale-to-width-down/120?cb=20180831204518",
    "Dawnbreaker": "https://static.wikia.nocookie.net/dota2_gamepedia/images/d/d6/Dawnbreaker_icon.png/revision/latest/scale-to-width-down/120?cb=20210410124439",
    "Dazzle": "https://static.wikia.nocookie.net/dota2_gamepedia/images/e/e6/Dazzle_icon.png/revision/latest/scale-to-width-down/120?cb=20160411220519",
    "Death Prophet": "https://static.wikia.nocookie.net/dota2_gamepedia/images/d/d7/Death_Prophet_icon.png/revision/latest/scale-to-width-down/120?cb=20160411220408",
    "Disruptor": "https://static.wikia.nocookie.net/dota2_gamepedia/images/9/97/Disruptor_icon.png/revision/latest/scale-to-width-down/120?cb=20160411215651",
    "Doom": "https://static.wikia.nocookie.net/dota2_gamepedia/images/4/40/Doom_icon.png/revision/latest/scale-to-width-down/120?cb=20160411212104",
    "Dragon Knight": "https://static.wikia.nocookie.net/dota2_gamepedia/images/5/59/Dragon_Knight_icon.png/revision/latest/scale-to-width-down/120?cb=20160411205925",
    "Drow Ranger": "https://static.wikia.nocookie.net/dota2_gamepedia/images/8/80/Drow_Ranger_icon.png/revision/latest/scale-to-width-down/120?cb=20190325143546",
    "Earth Spirit": "https://static.wikia.nocookie.net/dota2_gamepedia/images/b/be/Earth_Spirit_icon.png/revision/latest/scale-to-width-down/120?cb=20160411211247",
    "Earthshaker": "https://static.wikia.nocookie.net/dota2_gamepedia/images/a/a5/Earthshaker_icon.png/revision/latest/scale-to-width-down/120?cb=20160411205323",
    "Elder Titan": "https://static.wikia.nocookie.net/dota2_gamepedia/images/1/1a/Elder_Titan_icon.png/revision/latest/scale-to-width-down/120?cb=20160411210922",
    "Ember Spirit": "https://static.wikia.nocookie.net/dota2_gamepedia/images/9/91/Ember_Spirit_icon.png/revision/latest/scale-to-width-down/120?cb=20170417182614",
    "Enchantress": "https://static.wikia.nocookie.net/dota2_gamepedia/images/4/41/Enchantress_icon.png/revision/latest/scale-to-width-down/120?cb=20160411215320",
    "Enigma": "https://static.wikia.nocookie.net/dota2_gamepedia/images/f/f7/Enigma_icon.png/revision/latest/scale-to-width-down/120?cb=20160411220156",
    "Faceless Void": "https://static.wikia.nocookie.net/dota2_gamepedia/images/7/73/Faceless_Void_icon.png/revision/latest/scale-to-width-down/120?cb=20160411213936",
    "Grimstroke": "https://static.wikia.nocookie.net/dota2_gamepedia/images/d/d7/Grimstroke_icon.png/revision/latest/scale-to-width-down/120?cb=20180831203927",
    "Gyrocopter": "https://static.wikia.nocookie.net/dota2_gamepedia/images/4/4f/Gyrocopter_icon.png/revision/latest/scale-to-width-down/120?cb=20181101233643",
    "Hoodwink": "https://static.wikia.nocookie.net/dota2_gamepedia/images/c/c9/Hoodwink_icon.png/revision/latest/scale-to-width-down/120?cb=20201217205959",
    "Huskar": "https://static.wikia.nocookie.net/dota2_gamepedia/images/d/d3/Huskar_icon.png/revision/latest/scale-to-width-down/120?cb=20160411210201",
    "Invoker": "https://static.wikia.nocookie.net/dota2_gamepedia/images/0/00/Invoker_icon.png/revision/latest/scale-to-width-down/120?cb=20160411220849",
    "Io": "https://static.wikia.nocookie.net/dota2_gamepedia/images/8/8d/Io_icon.png/revision/latest/scale-to-width-down/120?cb=20160411210451",
    "Jakiro": "https://static.wikia.nocookie.net/dota2_gamepedia/images/2/2f/Jakiro_icon.png/revision/latest/scale-to-width-down/120?cb=20170507134250",
    "Juggernaut": "https://static.wikia.nocookie.net/dota2_gamepedia/images/0/03/Juggernaut_icon.png/revision/latest/scale-to-width-down/120?cb=20160411212710",
    "Keeper of the Light": "https://static.wikia.nocookie.net/dota2_gamepedia/images/b/b9/Keeper_of_the_Light_icon.png/revision/latest/scale-to-width-down/120?cb=20160411215721",
    "Kunkka": "https://static.wikia.nocookie.net/dota2_gamepedia/images/c/c0/Kunkka_icon.png/revision/latest/scale-to-width-down/120?cb=20160411205729",
    "Legion Commander": "https://static.wikia.nocookie.net/dota2_gamepedia/images/a/a2/Legion_Commander_icon.png/revision/latest/scale-to-width-down/120?cb=20190401095109",
    "Leshrac": "https://static.wikia.nocookie.net/dota2_gamepedia/images/2/26/Leshrac_icon.png/revision/latest/scale-to-width-down/120?cb=20160411220559",
    "Lich": "https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bb/Lich_icon.png/revision/latest/scale-to-width-down/120?cb=20160411215954",
    "Lifestealer": "https://static.wikia.nocookie.net/dota2_gamepedia/images/2/2b/Lifestealer_icon.png/revision/latest/scale-to-width-down/120?cb=20160411211952",
    "Lina": "https://static.wikia.nocookie.net/dota2_gamepedia/images/3/35/Lina_icon.png/revision/latest/scale-to-width-down/120?cb=20160411215059",
    "Lion": "https://static.wikia.nocookie.net/dota2_gamepedia/images/b/b8/Lion_icon.png/revision/latest/scale-to-width-down/120?cb=20160411220032",
    "Lone Druid": "https://static.wikia.nocookie.net/dota2_gamepedia/images/5/5d/Lone_Druid_icon.png/revision/latest/scale-to-width-down/120?cb=20160411213427",
    "Luna": "https://static.wikia.nocookie.net/dota2_gamepedia/images/7/7d/Luna_icon.png/revision/latest/scale-to-width-down/120?cb=20160411213209",
    "Lycan": "https://static.wikia.nocookie.net/dota2_gamepedia/images/d/d6/Lycan_icon.png/revision/latest/scale-to-width-down/120?cb=20160411212224",
    "Magnus": "https://static.wikia.nocookie.net/dota2_gamepedia/images/b/ba/Magnus_icon.png/revision/latest/scale-to-width-down/120?cb=20160411212403",
    "Marci": "https://static.wikia.nocookie.net/dota2_gamepedia/images/1/12/Marci_icon.png/revision/latest/scale-to-width-down/120?cb=20211029000514",
    "Mars": "https://static.wikia.nocookie.net/dota2_gamepedia/images/9/9d/Mars_icon.png/revision/latest/scale-to-width-down/120?cb=20190401094550",
    "Medusa": "https://static.wikia.nocookie.net/dota2_gamepedia/images/c/cc/Medusa_icon.png/revision/latest/scale-to-width-down/120?cb=20160411214604",
    "Meepo": "https://static.wikia.nocookie.net/dota2_gamepedia/images/8/85/Meepo_icon.png/revision/latest/scale-to-width-down/120?cb=20160411214421",
    "Mirana": "https://static.wikia.nocookie.net/dota2_gamepedia/images/1/12/Mirana_icon.png/revision/latest/scale-to-width-down/120?cb=20160411212744",
    "Monkey King": "https://static.wikia.nocookie.net/dota2_gamepedia/images/7/7b/Monkey_King_icon.png/revision/latest/scale-to-width-down/120?cb=20161222035035",
    "Morphling": "https://static.wikia.nocookie.net/dota2_gamepedia/images/7/7b/Morphling_icon.png/revision/latest/scale-to-width-down/120?cb=20160411212816",
    "Naga Siren": "https://static.wikia.nocookie.net/dota2_gamepedia/images/6/60/Naga_Siren_icon.png/revision/latest/scale-to-width-down/120?cb=20160411213513",
    "Necrophos": "https://static.wikia.nocookie.net/dota2_gamepedia/images/a/a6/Necrophos_icon.png/revision/latest/scale-to-width-down/120?cb=20160411220233",
    "Night Stalker": "https://static.wikia.nocookie.net/dota2_gamepedia/images/1/15/Night_Stalker_icon.png/revision/latest/scale-to-width-down/120?cb=20160411212027",
    "Nyx Assassin": "https://static.wikia.nocookie.net/dota2_gamepedia/images/f/fa/Nyx_Assassin_icon.png/revision/latest/scale-to-width-down/120?cb=20160411214454",
    "Ogre Magi": "https://static.wikia.nocookie.net/dota2_gamepedia/images/e/e0/Ogre_Magi_icon.png/revision/latest/scale-to-width-down/120?cb=20160411215538",
    "Omniknight": "https://static.wikia.nocookie.net/dota2_gamepedia/images/e/e2/Omniknight_icon.png/revision/latest/scale-to-width-down/120?cb=20160411210119",
    "Oracle": "https://static.wikia.nocookie.net/dota2_gamepedia/images/7/72/Oracle_icon.png/revision/latest/scale-to-width-down/120?cb=20160411215824",
    "Outworld Destroyer": "https://static.wikia.nocookie.net/dota2_gamepedia/images/1/10/Outworld_Destroyer_icon.png/revision/latest/scale-to-width-down/120?cb=20160411220923",
    "Pangolier": "https://static.wikia.nocookie.net/dota2_gamepedia/images/4/4e/Pangolier_icon.png/revision/latest/scale-to-width-down/120?cb=20180831204401",
    "Phantom Assassin": "https://static.wikia.nocookie.net/dota2_gamepedia/images/8/8e/Phantom_Assassin_icon.png/revision/latest/scale-to-width-down/120?cb=20160411214013",
    "Phantom Lancer": "https://static.wikia.nocookie.net/dota2_gamepedia/images/8/81/Phantom_Lancer_icon.png/revision/latest/scale-to-width-down/120?cb=20160411212849",
    "Phoenix": "https://static.wikia.nocookie.net/dota2_gamepedia/images/1/14/Phoenix_icon.png/revision/latest/scale-to-width-down/120?cb=20160411211344",
    "Primal Beast": "https://static.wikia.nocookie.net/dota2_gamepedia/images/f/f2/Primal_Beast_icon.png/revision/latest/scale-to-width-down/120?cb=20220223230622",
    "Puck": "https://static.wikia.nocookie.net/dota2_gamepedia/images/1/13/Puck_icon.png/revision/latest/scale-to-width-down/120?cb=20160411214839",
    "Pudge": "https://static.wikia.nocookie.net/dota2_gamepedia/images/c/c0/Pudge_icon.png/revision/latest/scale-to-width-down/120?cb=20160411211506",
    "Pugna": "https://static.wikia.nocookie.net/dota2_gamepedia/images/c/cd/Pugna_icon.png/revision/latest/scale-to-width-down/120?cb=20160411220442",
    "Queen of Pain": "https://static.wikia.nocookie.net/dota2_gamepedia/images/a/a1/Queen_of_Pain_icon.png/revision/latest/scale-to-width-down/120?cb=20160411220334",
    "Razor": "https://static.wikia.nocookie.net/dota2_gamepedia/images/6/66/Razor_icon.png/revision/latest/scale-to-width-down/120?cb=20160411213830",
    "Riki": "https://static.wikia.nocookie.net/dota2_gamepedia/images/7/7d/Riki_icon.png/revision/latest/scale-to-width-down/120?cb=20160411212958",
    "Rubick": "https://static.wikia.nocookie.net/dota2_gamepedia/images/8/8a/Rubick_icon.png/revision/latest/scale-to-width-down/120?cb=20160411215614",
    "Sand King": "https://static.wikia.nocookie.net/dota2_gamepedia/images/7/79/Sand_King_icon.png/revision/latest/scale-to-width-down/120?cb=20160411211544",
    "Shadow Demon": "https://static.wikia.nocookie.net/dota2_gamepedia/images/f/f3/Shadow_Demon_icon.png/revision/latest/scale-to-width-down/120?cb=20160411220956",
    "Shadow Fiend": "https://static.wikia.nocookie.net/dota2_gamepedia/images/3/36/Shadow_Fiend_icon.png/revision/latest/scale-to-width-down/120?cb=20160411213752",
    "Shadow Shaman": "https://static.wikia.nocookie.net/dota2_gamepedia/images/9/96/Shadow_Shaman_icon.png/revision/latest/scale-to-width-down/120?cb=20160411215130",
    "Silencer": "https://static.wikia.nocookie.net/dota2_gamepedia/images/9/9f/Silencer_icon.png/revision/latest/scale-to-width-down/120?cb=20160411215503",
    "Skywrath Mage": "https://static.wikia.nocookie.net/dota2_gamepedia/images/b/bf/Skywrath_Mage_icon.png/revision/latest/scale-to-width-down/120?cb=20160411215753",
    "Slardar": "https://static.wikia.nocookie.net/dota2_gamepedia/images/7/7e/Slardar_icon.png/revision/latest/scale-to-width-down/120?cb=20161213040814",
    "Slark": "https://static.wikia.nocookie.net/dota2_gamepedia/images/a/aa/Slark_icon.png/revision/latest/scale-to-width-down/120?cb=20160411214526",
    "Snapfire": "https://static.wikia.nocookie.net/dota2_gamepedia/images/7/7a/Snapfire_icon.png/revision/latest/scale-to-width-down/120?cb=20191127043227",
    "Sniper": "https://static.wikia.nocookie.net/dota2_gamepedia/images/5/51/Sniper_icon.png/revision/latest/scale-to-width-down/120?cb=20160411213053",
    "Spectre": "https://static.wikia.nocookie.net/dota2_gamepedia/images/f/ff/Spectre_icon.png/revision/latest/scale-to-width-down/120?cb=20160411214336",
    "Spirit Breaker": "https://static.wikia.nocookie.net/dota2_gamepedia/images/d/df/Spirit_Breaker_icon.png/revision/latest/scale-to-width-down/120?cb=20160411212138",
    "Storm Spirit": "https://static.wikia.nocookie.net/dota2_gamepedia/images/1/13/Storm_Spirit_icon.png/revision/latest/scale-to-width-down/120?cb=20160411214914",
    "Sven": "https://static.wikia.nocookie.net/dota2_gamepedia/images/1/1b/Sven_icon.png/revision/latest/scale-to-width-down/120?cb=20160411205500",
    "Techies": "https://static.wikia.nocookie.net/dota2_gamepedia/images/f/fa/Techies_icon.png/revision/latest/scale-to-width-down/120?cb=20160411215855",
    "Templar Assassin": "https://static.wikia.nocookie.net/dota2_gamepedia/images/9/9c/Templar_Assassin_icon.png/revision/latest/scale-to-width-down/120?cb=20160411213131",
    "Terrorblade": "https://static.wikia.nocookie.net/dota2_gamepedia/images/5/52/Terrorblade_icon.png/revision/latest/scale-to-width-down/120?cb=20160411214652",
    "Tidehunter": "https://static.wikia.nocookie.net/dota2_gamepedia/images/d/d5/Tidehunter_icon.png/revision/latest/scale-to-width-down/120?cb=20160411211651",
    "Timbersaw": "https://static.wikia.nocookie.net/dota2_gamepedia/images/9/9a/Timbersaw_icon.png/revision/latest/scale-to-width-down/120?cb=20160411210643",
    "Tinker": "https://static.wikia.nocookie.net/dota2_gamepedia/images/d/d1/Tinker_icon.png/revision/latest/scale-to-width-down/120?cb=20160411215201",
    "Tiny": "https://static.wikia.nocookie.net/dota2_gamepedia/images/5/55/Tiny_icon.png/revision/latest/scale-to-width-down/120?cb=20160411205608",
    "Treant Protector": "https://static.wikia.nocookie.net/dota2_gamepedia/images/3/3f/Treant_Protector_icon.png/revision/latest/scale-to-width-down/120?cb=20160411210417",
    "Troll Warlord": "https://static.wikia.nocookie.net/dota2_gamepedia/images/f/f0/Troll_Warlord_icon.png/revision/latest/scale-to-width-down/120?cb=20160411213539",
    "Tusk": "https://static.wikia.nocookie.net/dota2_gamepedia/images/c/ce/Tusk_icon.png/revision/latest/scale-to-width-down/120?cb=20160411210826",
    "Underlord": "https://static.wikia.nocookie.net/dota2_gamepedia/images/1/18/Underlord_icon.png/revision/latest/scale-to-width-down/120?cb=20160828140759",
    "Undying": "https://static.wikia.nocookie.net/dota2_gamepedia/images/6/61/Undying_icon.png/revision/latest/scale-to-width-down/120?cb=20160411212333",
    "Ursa": "https://static.wikia.nocookie.net/dota2_gamepedia/images/4/40/Ursa_icon.png/revision/latest/scale-to-width-down/120?cb=20160411213321",
    "Vengeful Spirit": "https://static.wikia.nocookie.net/dota2_gamepedia/images/2/20/Vengeful_Spirit_icon.png/revision/latest/scale-to-width-down/120?cb=20160411212927",
    "Venomancer": "https://static.wikia.nocookie.net/dota2_gamepedia/images/2/25/Venomancer_icon.png/revision/latest/scale-to-width-down/120?cb=20160411213902",
    "Viper": "https://static.wikia.nocookie.net/dota2_gamepedia/images/5/5f/Viper_icon.png/revision/latest/scale-to-width-down/120?cb=20161213040756",
    "Visage": "https://static.wikia.nocookie.net/dota2_gamepedia/images/9/9e/Visage_icon.png/revision/latest/scale-to-width-down/120?cb=20160411221032",
    "Void Spirit": "https://static.wikia.nocookie.net/dota2_gamepedia/images/9/99/Void_Spirit_icon.png/revision/latest/scale-to-width-down/120?cb=20210413204208",
    "Warlock": "https://static.wikia.nocookie.net/dota2_gamepedia/images/3/3f/Warlock_icon.png/revision/latest/scale-to-width-down/120?cb=20160411220306",
    "Weaver": "https://static.wikia.nocookie.net/dota2_gamepedia/images/0/09/Weaver_icon.png/revision/latest/scale-to-width-down/120?cb=20160411214233",
    "Windranger": "https://static.wikia.nocookie.net/dota2_gamepedia/images/6/60/Windranger_icon.png/revision/latest/scale-to-width-down/120?cb=20160411214951",
    "Winter Wyvern": "https://static.wikia.nocookie.net/dota2_gamepedia/images/4/4a/Winter_Wyvern_icon.png/revision/latest/scale-to-width-down/120?cb=20160411221057",
    "Witch Doctor": "https://static.wikia.nocookie.net/dota2_gamepedia/images/3/33/Witch_Doctor_icon.png/revision/latest/scale-to-width-down/120?cb=20160411220105",
    "Wraith King": "https://static.wikia.nocookie.net/dota2_gamepedia/images/1/1e/Wraith_King_icon.png/revision/latest/scale-to-width-down/120?cb=20160411211746",
    "Zeus": "https://static.wikia.nocookie.net/dota2_gamepedia/images/3/3f/Zeus_icon.png/revision/latest/scale-to-width-down/120?cb=20160411215025"
}

insert_query = "UPDATE dota_track.heroes_data set scoreboard_icon_url='{}' WHERE localized_name='{}'"

for hero in heroes:
    name = hero['localized_name']
    if name != "Nature's Prophet":
        cursor.execute(insert_query.format(HERO_ID_TO_PIC_URL[name], name))

connection.commit()


