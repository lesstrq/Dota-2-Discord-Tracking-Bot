ARROW_DOUBLE_UP = ":arrow_double_up:"
ARROW_DOUBLE_DOWN = ":arrow_double_down:"
ARROW_UP_SMALL = ":arrow_up_small:"
ARROW_DOWN_SMALL = ":arrow_down_small:"
MAN_BUST = ":bust_in_silhouette:"
WHITE_CHECK_MARK_GREEN_BACKGROUND = ":white_check_mark:"
RED_CROSS_WRONG = ":x:"
MONEY_WITH_WINGS = ":money_with_wings:"
CROSSED_SWORDS = ":crossed_swords:"
HAMMER = ":hammer:"
FIRST_PLACE = ":first_place:"
SECOND_PLACE = ":second_place:"
THIRD_PLACE = ":third_place:"
MENDING_HEART = ":mending_heart:"
CLOCK = ":clock4:"
SCALES = ":scales:"


def choose_kda_emoji(game_kda, avg_kda):
    if game_kda > avg_kda * 2:
        kda_emoji = ARROW_DOUBLE_UP
    elif game_kda >= avg_kda:
        kda_emoji = ARROW_UP_SMALL
    elif game_kda < avg_kda / 2:
        kda_emoji = ARROW_DOUBLE_DOWN
    else:
        kda_emoji = ARROW_DOWN_SMALL

    return kda_emoji


def create_party_size_line(party_size):
    return MAN_BUST * party_size


def win_or_lose_emoji(result):
    return WHITE_CHECK_MARK_GREEN_BACKGROUND if result == 'Win' else RED_CROSS_WRONG


def top_emoji(values, player_value):
    emojis = [FIRST_PLACE, SECOND_PLACE, THIRD_PLACE]
    player_place = values.index(player_value)

    return emojis[player_place] if player_place < 3 else ""

