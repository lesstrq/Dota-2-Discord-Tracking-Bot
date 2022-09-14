from PIL import Image

template = Image.open("assets/items/template.png")
item_id = 208
bf = Image.open(f"assets/items/{item_id}.png")

slot_coord = {0: (6, 7),
              1: (72, 7),
              2: (138, 7),
              3: (6, 55),
              4: (72, 55),
              5: (138, 55),
              6: (6, 104),
              7: (72, 104),
              8: (138, 104)}

new_image = template.copy()
for i in range(9):
    if i > 5:
        bf = Image.open("assets/items/208.png")
        bf = bf.convert("L")
        bf = bf.crop((1, 6, 60, 38))
    new_image.paste(bf, slot_coord[i])

new_image.save("assets/trial.png", quality=100)
