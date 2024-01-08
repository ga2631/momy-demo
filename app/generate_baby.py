import requests
import shutil
import time
import torch
from diffusers import DiffusionPipeline

def detect_face(image_name):
    API_URL = "https://api.faceshape.com/infer_img/faceshape_full"
    TOKEN = ""
    HEADERS = {
        "Authorization": "Bearer " + TOKEN
    }

    response = requests.post(API_URL, headers=HEADERS, files={'file': open('static/imgs/' + image_name, 'rb')})
    if not (200 == response.status_code):
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
    API_TOKEN = ""

    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    payload = { "inputs": prompt }
    response = requests.post(API_URL, headers=headers, json=payload, stream=True)

    if 200 == response.status_code:
        filename = 'img_' + time.strftime("%Y%m%d%H%M%S") + '.png'
        file_path = 'static/imgs/' + filename
        with open(file_path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        
        return filename
    
    print("generate_baby_with_api", response.json())

    return False

def generate_baby_with_model(_prompt):
    pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
    pipe.to("mps")

    images = pipe(prompt=_prompt).images[0]
    print(images)
    # if(not images):
    #     return False
    
    # filename = 'img_' + time.strftime("%Y%m%d%H%M%S") + '.png'
    # file_path = 'static/imgs/' + filename
    # images.save(file_path) 

    # return filename

# def fx_cartoon():
