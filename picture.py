import requests
from PIL import Image
from PIL import ImageDraw
import random
from  abilities_ids import ABILITIES_IDS

slots = ["item_0", "item_1", "item_2", "item_3", "item_4", "item_5", "backpack_0", "backpack_1", "backpack_2", "item_neutral"]


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

def create_image(items):
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
    inventory.save(f"assets/{filename}.png", quality=100)
    return f"assets/{filename}.png"

def create_skill_build_image(abilities):
    ability_slot = Image.open("assets/abilities/ability_slot.png")
    field = mul_concat(ability_slot, len(abilities))
    for i, ability in enumerate(abilities):
        ability_name = ABILITIES_IDS[str(ability)]
        ability_image = Image.open(f"assets/abilities/{ability_name}.png")
        field.paste(ability_image, (5 + i * 50, 5))
    field.save("assets/trial.png")

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

ability_upgrades_arr = [
            5286,
            5285,
            5286,
            5285,
            5286,
            5288,
            5286,
            5285,
            5285,
            5287,
            484,
            5288,
            5287,
            5287,
            876,
            5287,
            5288,
            6018,
            877,
            869,
            959,
            878
         ]
create_skill_build_image(ability_upgrades_arr)