import time
import datetime
from table2ascii import table2ascii, TableStyle, Alignment

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

def create_table():
    my_style = TableStyle.from_string('╔═╦╦╗║║║╟─╫╫╢╟═╫╫╫╚═╩╝')
    table = table2ascii(
        header=['Level:'] + list(range(1, 11)),
        body=[['Ability:', 1, 2, 1, 2, 1, 4, 1, 2, 2, 'L']],
        style=my_style,
        alignments=[Alignment.LEFT] + [Alignment.CENTER for _ in range(10)]
    )
    return table

print(create_table())