from PIL import Image
import requests
import shutil
import os

url = "https://api.opendota.com/api/constants/abilities"

abilities_data = requests.get(url).json()

def write_image(image_url, image_name):
    img_data = requests.get(image_url, stream=True).raw
    with open(f'C:/Users/omg11/Documents/GitHub/Dota-2-Discord-Tracking-Bot/assets/abilities/{image_name}.jpg', 'wb') as handler:
        shutil.copyfileobj(img_data, handler)
    current = Image.open(f'C:/Users/omg11/Documents/GitHub/Dota-2-Discord-Tracking-Bot/assets/abilities/{image_name}.jpg')
    current = current.resize((40, 40))
    current.save(f'C:/Users/omg11/Documents/GitHub/Dota-2-Discord-Tracking-Bot/assets/abilities/{image_name}.png')
    os.remove(f'C:/Users/omg11/Documents/GitHub/Dota-2-Discord-Tracking-Bot/assets/abilities/{image_name}.jpg')

for ability in abilities_data:
    try:
        print(ability)
        print(abilities_data[ability])
        img_url = f"https://api.opendota.com{abilities_data[ability]['img']}"
        print(img_url)
        write_image(img_url, ability)
    except Exception as e:
        print(e)
        continue