from PIL import Image
from PIL import ImageDraw
import random
from abilities_ids import ABILITIES_IDS
from misc import hero_id_from_ability_id
from constants.heroes import heroes
from constants.hero_abilities import hero_abilities

DIRECTORY_TO_SAVE_IN = "temporary_pictures/"

slots = ["item_0", "item_1", "item_2",
         "item_3", "item_4", "item_5",
         "backpack_0", "backpack_1", "backpack_2",
         "item_neutral"]

slot_coord = {"item_0": (6, 7),
              "item_1": (72, 7),
              "item_2": (138, 7),
              "item_3": (6, 55),
              "item_4": (72, 55),
              "item_5": (138, 55),
              "backpack_0": (6, 104),
              "backpack_1": (72, 104),
              "backpack_2": (138, 104),
              "item_neutral": (193, 32)}


def create_image(player):
    items = {}
    for slot in slots:
        items[slot] = player[slot]
    mask_im = Image.new("L", (60, 43), 0)
    draw = ImageDraw.Draw(mask_im)
    draw.ellipse((8, 1, 52, 42), fill=255)
    inventory = Image.open("assets/items/template.png")
    for slot in items:
        if items[slot] == 0:
            continue
        item_img = Image.open(f"assets/items/{items[slot]}.png")
        if "backpack" in slot:
            item_img = item_img.convert("L")
            item_img = item_img.crop((1, 6, 60, 38))
        if "neutral" in slot:
            inventory.paste(item_img, (194, 32), mask_im)
            continue
        inventory.paste(item_img, slot_coord[slot])
    filename = random.randint(1000000, 9999999)
    inventory.save(f"{DIRECTORY_TO_SAVE_IN}{filename}.png", quality=100)
    return f"{DIRECTORY_TO_SAVE_IN}{filename}.png"


def left_or_right_talent(abilities_info, ability_name):
    for i in range(1, 9):
        if abilities_info["talents"][i - 1]["name"] == ability_name:
            return "right" if i % 2 else "left"


def create_skill_build_image(abilities, level):
    temp = []
    i = 0
    j = 1
    while len(temp) != level:
        if j + 1 in [17, 19, 21, 22, 23, 24, 26]:
            temp.append(-1)
        else:
            temp.append(abilities[i])
            i += 1
        j += 1
    abilities = temp
    ability_slot = Image.open("assets/abilities/ability_slot.png")
    field = mul_concat(ability_slot, len(abilities))
    abilities_info = hero_abilities[heroes[str(hero_id_from_ability_id(str(abilities[0])))]["name"]]
    for i, ability in enumerate(abilities):
        if ability == -1:
            ability_image = Image.open("assets/abilities/attrs.png")
            field.paste(ability_image, (5 + i * 50, 5))
            continue
        ability_name = ABILITIES_IDS[str(ability)]
        if "special_bonus" in ability_name:
            ability_image = Image.open(
                f"assets/abilities/{left_or_right_talent(abilities_info, ability_name)}_talent_placeholder.png")
        else:
            ability_image = Image.open(f"assets/abilities/{ability_name}.png")
        field.paste(ability_image, (5 + i * 50, 5))
    field.save("assets/trial.png")
    filename = random.randint(1000000, 9999999)
    field.save(f"assets/{filename}.png", quality=100)
    return f"assets/{filename}.png"


def concatenate(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


def mul_concat(image, times):
    picture = image.copy()
    for i in range(times - 1):
        picture = concatenate(picture, image)
    return picture
