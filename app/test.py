import os
import uuid
from PIL import Image
from io import BytesIO
import requests
from services.useapi import UseApi
from services.discord import Discord

def crop_image(image, image_path, x, y, w = 512, h = 512):
    response = requests.get(image)
    image = Image.open(BytesIO(response.content))

    # Crop the image
    cropped_image = image.crop((x, y, w, h))

    # Save the cropped image
    cropped_image.save(image_path)
    
    return image_path

def main(mom_img_url : str, dad_img_url : str, sex : str = 'male', mom_rate : int = 50, dad_rate : int = 50):
    request_id = uuid.uuid4()
    
    prompt = "{} {} simple sticker cartoon neonate {} face, neonate boy face is smiling, image 1 similar rate is {}% and image 2 similar rate is {}% in white background, simple graphic design, symmetrical, 300 dpi, –-no glasses, –-no mockup --v 4 --s 750".format(mom_img_url, dad_img_url, sex, mom_rate, dad_rate)
    
    print("PROMPT : {}".format(prompt))

    print("Generating...")
    useapi = UseApi()
    imagine_response = useapi.imagine(prompt)
    
    image_url = imagine_response.attachments[0].url
    print("GENERATE_IMAGE_URL : {}".format(image_url))

    image_paths = list([])
        
    image_path_1 = os.path.abspath(f'static/imgs/generated/{request_id}_1.png')
    image_paths.append(crop_image(image_url, image_path_1, 0, 0))
    
    image_path_2 = os.path.abspath(f'static/imgs/generated/{request_id}_2.png')
    image_paths.append(crop_image(image_url, image_path_2, 513, 0, 1024))
    
    image_path_3 = os.path.abspath(f'static/imgs/generated/{request_id}_3.png')
    image_paths.append(crop_image(image_url, image_path_3, 0, 513, 512, 1024))
    
    image_path_4 = os.path.abspath(f'static/imgs/generated/{request_id}_4.png')
    image_paths.append(crop_image(image_url, image_path_4, 513, 513, 1024, 1024))
    
    print("IMAGE_PATHS : {}".format(image_paths.__str__()))

    pass

def generate_baby():
    mom_file_path = 'static/imgs/upload/412039575_3645580589019831_3979029158204138001_n.jpg'
    dad_file_path = 'static/imgs/upload/IMG_4029.jpeg'
    file_paths = list([mom_file_path, dad_file_path])
    print("IMAGE IS UPLOADING...")
    
    discord = Discord()
    attachment_urls = discord.upload('1195296642174300322', file_paths = file_paths)
    
    main(mom_img_url = attachment_urls[0], dad_img_url = attachment_urls[1], mom_rate = 50, dad_rate = 50, sex = 'female')

generate_baby()