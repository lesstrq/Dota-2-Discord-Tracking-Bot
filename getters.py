import requests
from constants.heroes import heroes
import misc

OPENDOTA_API_URL = "https://api.opendota.com/api/"
player_slots = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 128: 5, 129: 6, 130: 7, 131: 8, 132: 9}


def get_nickname_by_dota_id(dota_id):
    return requests.get(OPENDOTA_API_URL + f"players/{dota_id}").json()["profile"]["personaname"]


class Player:
    def __init__(self, dota_id):
        self.dota_id = dota_id
        self.info = requests.get(OPENDOTA_API_URL + f"players/{dota_id}").json()
        self.wins, self.loses = requests.get(OPENDOTA_API_URL + f"players/{dota_id}/wl").json().values()

    def get_nickname(self):
        return self.info["profile"]["personaname"]

    def get_wins(self):
        return self.wins

    def get_loses(self):
        return self.loses

    def get_winrate(self):
        return round(100 * (self.get_wins() / (self.get_wins() + self.get_loses())), 2)

    def get_rank(self):
        return misc.get_rank(self.info['rank_tier'])

    def is_on_leaderboard(self):
        return bool(self.info['leaderboard_rank'])

    def get_leaderboard_rank(self):
        if self.is_on_leaderboard():
            return self.info['leaderboard_rank']
        return ""

    def get_avatar_url(self):
        return self.info["profile"]["avatarfull"]


class RecentGame:
    def __init__(self, dota_id):
        self.dota_id = dota_id
        self.info = requests.get(OPENDOTA_API_URL + f"players/{dota_id}/matches?limit=1").json()[0]
        self.detailed_info = requests.get(f"http://api.opendota.com/api/matches/{self.info['match_id']}").json()

    def get_hero_id(self):
        return str(self.info['hero_id'])

    def get_hero_name(self):
        return heroes[self.get_hero_id()]['localized_name']

    def get_hero_image_url(self):
        return OPENDOTA_API_URL[:-5] + heroes[self.get_hero_id()]['img']

    def get_player_slot(self):
        return self.info['player_slot']

    def get_net_worth(self):
        return self.detailed_info['players'][player_slots[self.get_player_slot()]]['net_worth']

    def get_hero_damage(self):
        return self.detailed_info['players'][player_slots[self.get_player_slot()]]['hero_damage']

    def get_kills(self):
        return self.info['kills']

    def get_assists(self):
        return self.info['assists']

    def get_deaths(self):
        return self.info['deaths']

    def get_kda(self):
        return (self.get_kills() + self.get_assists()) / (self.get_deaths() or 1)

    def get_result(self):
        game_info = self.info
        result = "Win" if (game_info['player_slot'] > 100 and not game_info['radiant_win']) or (
                game_info['player_slot'] < 100 and game_info['radiant_win']) else "Lose"

        return result

    def get_avg_kda(self):
        dota_id = self.dota_id
        hero_id = self.get_hero_id()
        all_games_info = requests.get(
            OPENDOTA_API_URL + f'players/{dota_id}/matches?hero_id={hero_id}').json()
        kills, deaths, assists = 0, 0, 0
        for match in all_games_info:
            kills += match["kills"]
            deaths += match["deaths"]
            assists += match["assists"]
        avg_kda = (kills + assists) / (deaths or 1)

        return avg_kda

    def get_duration(self):
        game_info = self.info
        duration = {'mins': ("0" if game_info['duration'] % 60 < 10 else "") + str(game_info['duration'] // 60),
                    'secs': ("0" if game_info['duration'] % 60 < 10 else "") + str(game_info['duration'] % 60)}

        return duration

    def get_lobby_size(self):
        lobby_size = self.info['party_size']

        return lobby_size

    def get_players(self):
        return self.detailed_info['players']

    def get_player_detailed_info(self):
        return self.detailed_info['players'][player_slots[self.get_player_slot()]]