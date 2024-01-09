import requests
import shutil
import time
import os
from token_api import FACESHAPE_TOKEN, HUGGINGFACE_API_TOKEN

def detect_face(image_name):
    API_URL = "https://api.faceshape.com/infer_img/faceshape_full"
    HEADERS = {
        "Authorization": "Bearer " + FACESHAPE_TOKEN
    }
    FILES = {
        "file": open('static/imgs/' + image_name, 'rb')
    }

    response = requests.post(API_URL, headers=HEADERS, files=FILES)
    if 200 != response.status_code:
        print(response.json())

        return False

    json = response.json()

    face_detect = []
    faceshape = json['faces'][0]['faceshape']
    if(faceshape):
        faceshape_str = ' and '.join(faceshape) + ' face shape'
        face_detect.append(faceshape_str)

    jaw = json['faces'][0]['jaw']
    if(jaw):
        face_detect.append(jaw + ' jaw')

    facelength = json['faces'][0]['facelength']
    if(facelength):
        face_detect.append(facelength + ' face length')

    return face_detect

def generate_baby_with_api(prompt):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    HEADERS = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
    }
    PAYLOAD = { 
        "inputs": prompt 
    }

    response = requests.post(API_URL, headers=HEADERS, json=PAYLOAD, stream=True)

    if 200 == response.status_code:
        filename = 'img_' + time.strftime("%Y%m%d%H%M%S") + '.png'
        file_path = 'static/imgs/' + filename
        os.pardirs(file_path)
        with open(file_path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        
        return filename
    
    print("generate_baby_with_api", response.json())

    return False