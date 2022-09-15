import requests
from PIL import Image
from PIL import ImageDraw
import random

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


