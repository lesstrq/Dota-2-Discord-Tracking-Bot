from PIL import Image
import requests
import shutil
import os

items_data = requests.get("https://api.opendota.com/api/constants/items").json()

def write_image(image_url, image_name):
    img_data = requests.get(image_url, stream=True).raw
    with open(f'assets/items/{image_name}.jpg', 'wb') as handler:
        shutil.copyfileobj(img_data, handler)
    current = Image.open(f'assets/items/{image_name}.jpg')
    current = current.resize((60, 43))
    current.save(f'assets/items/{image_name}.png')
    os.remove(f'assets/items/{image_name}.jpg')


for item in items_data:
    print(items_data[item])
    item_id = str(items_data[item]['id'])
    img_url = f"https://api.opendota.com{items_data[item]['img']}"
    print(img_url)
    write_image(img_url, item_id)

