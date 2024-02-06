import os
from io import BytesIO
from requests import get as request_get
from uuid import uuid4
from base64 import b64decode
from timeit import default_timer as timer
from datetime import timedelta
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from PIL import Image
from services.discord import Discord
from services.useapi import UseApi
from configs.token import DISCORD_CHANNEL_ID

# import logging
# import logging.config

# config_file = path.abspath('configs/logging.conf')
# logging.config.fileConfig(config_file)
# logger = logging.getLogger('simpleExample')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)

class GenerateData(BaseModel):
    mom: str
    dad: str
    dad_percent: int = 0
    mom_percent: int = 100
    sex: str = 'girl'
    
class EmotionData(BaseModel):
    image: str
    sex: str

def save_image(base64_image : str, prefix : str = 'output', is_only_name : bool = False) -> str:
    decoded_bytes = b64decode(base64_image)
    image = Image.open(BytesIO(decoded_bytes))

    image_name = prefix + '_' + uuid4().hex + '.png'
    save_image_path = os.path.abspath(f'static/imgs/generated/{image_name}')
    image.save(save_image_path)
    
    if is_only_name:
        return image_name
    
    return save_image_path

def crop_image(image, image_file_name, x, y, w = 512, h = 512):
    response = request_get(image)
    image = Image.open(BytesIO(response.content))

    # Crop the image
    cropped_image = image.crop((x, y, w, h))

    # Save the cropped image
    image_path = os.path.abspath("static/imgs/generated/{}".format(image_file_name))
    cropped_image.save(image_path)
    
    return image_file_name

def upload_to_discord(file_location : str):
    discord = Discord()
    attachment_urls = discord.upload(channel_id = DISCORD_CHANNEL_ID, file_paths = list([file_location]))
        
    return attachment_urls
    

def generate_baby(generate: GenerateData):
    request_id = uuid4()
    
    mom_url = generate.mom
    dad_url = generate.dad
    sex = generate.sex
    mom_percent = generate.mom_percent
    dad_percent = generate.dad_percent
    
    prompt = f"{mom_url} {dad_url} a baby {sex}:: face, smiling, {mom_percent}% of first image and {dad_percent}% of second image, simple graphic design, in the style of flat shading, white background, bright tones, 8k resolution, high speed sync, --no glasses, sunglasses, mockup --style cute --s 300 --niji 5"
    
    print("PROMPT : {}".format(prompt))

    print("BABY IS GENERATING ...")
    
    start_time = timer()
    useapi = UseApi()
    imagine_response = useapi.imagine(prompt)
    end_time = timer()
    
    total_time = end_time - start_time
    print(f"GENERATE TIME : {total_time}")
    
    image_url = imagine_response.attachments[0].url
    print("GENERATE_IMAGE_URL : {}".format(image_url))

    print("IMAGE SPLITING...")
    start_time = timer()
    image_file_names = list([])
        
    image_file_name_1 = "{}_1.png".format(request_id)
    image_file_names.append(crop_image(image_url, image_file_name_1, 0, 0, 1024, 1024))
    
    image_file_name_2 = "{}_2.png".format(request_id)
    image_file_names.append(crop_image(image_url, image_file_name_2, 1025, 0, 2048, 1024))
    
    image_file_name_3 = "{}_3.png".format(request_id)
    image_file_names.append(crop_image(image_url, image_file_name_3, 0, 1025, 1025, 2048))
    
    image_file_name_4 = "{}_4.png".format(request_id)
    image_file_names.append(crop_image(image_url, image_file_name_4, 1025, 1025, 2048, 2048))
    end_time = timer()
    print("IMAGE SPLIT TIME : {}".format(end_time))
    
    print("IMAGE FILE NAMES : {}".format(image_file_names.__str__()))

    return image_file_names

def generate_emotions(data: EmotionData):
    filename_tmp = data.image
    file_location = f"static/imgs/generated/{filename_tmp}"
    
    attachment_urls = upload_to_discord(file_location)
    attachment_url = attachment_urls[0]
    
    sex = data.sex
    prompt = f"{attachment_url} a baby {sex} is shown at various emotions expressions with eyes and mouths, in the style of flat shading, white background, 8k resolution, high speed sync, 9 in 1, horizontal justify image --no mockup, sunglasses, glasses --style cute --s 100 --niji 5"
    
    print("PROMPT : {}".format(prompt))

    print("BABY IS GENERATING ...")
    
    start_time = timer()
    useapi = UseApi()
    imagine_response = useapi.imagine(prompt)
    end_time = timer()
    
    total_time = end_time - start_time
    print(f"GENERATE TIME : {total_time}")
    
    image_url = imagine_response.attachments[0].url
    print("GENERATE_IMAGE_URL : {}".format(image_url))

    print("IMAGE SPLITING...")
    start_time = timer()
    image_file_names = list([])

    filename_tmp.replace('.png', '')
    
    image_file_name_1 = "{}_emotion_1.png".format(filename_tmp)
    image_file_names.append(crop_image(image_url, image_file_name_1, 0, 0, 1024, 1024))
    
    image_file_name_2 = "{}_emotion_2.png".format(filename_tmp)
    image_file_names.append(crop_image(image_url, image_file_name_2, 1025, 0, 2048, 1024))
    
    image_file_name_3 = "{}_emotion_3.png".format(filename_tmp)
    image_file_names.append(crop_image(image_url, image_file_name_3, 0, 1025, 1025, 2048))
    
    image_file_name_4 = "{}_emotion_4.png".format(filename_tmp)
    image_file_names.append(crop_image(image_url, image_file_name_4, 1025, 1025, 2048, 2048))
    end_time = timer()
    print("IMAGE SPLIT TIME : {}".format(end_time))
    
    print("IMAGE FILE NAMES : {}".format(image_file_names.__str__()))

    return image_file_names

@app.get("/")
async def root():
    """
        This function is the root endpoint of the API.
        It is an asynchronous function that does not take any parameters.
        It returns a dictionary with a single key-value pair,
        where the key is "message" and the value is "Hello World".
    """
    return {"message": "Hello World"}

@app.get("/image")
async def get_image(file_name : str = ''):
    """
    A function that serves as the endpoint for the "/image" route.
    This function does not take any parameters and does not return anything.
    """
    print(file_name)
    if '' == file_name:
        response = {
            'error': 'no file name'
        }
        return JSONResponse(content = response)
    
    path = os.path.abspath("static/imgs/generated/{}".format(file_name))
    return FileResponse(path=path)

@app.post("/upload")
async def upload_file(file: UploadFile):
    """
    Uploads a file to the server.

    Parameters:
    - file: An instance of UploadFile representing the file to be uploaded.

    Returns:
    - A dictionary containing the following keys:
        - 'info': A string indicating the information about the uploaded file.
        - 'filename': A string representing the filename of the uploaded file.
    """
    filename_tmp = file.filename
    file_location = f"static/imgs/upload/{filename_tmp}"

    try:
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
    finally:
        file.file.close()

    attachment_urls = upload_to_discord(file_location)
        
    return {
        "info": f"file '{file.filename}' saved at '{file_location}'", 
        "filename": filename_tmp,
        "file_url": attachment_urls[0]
    }

@app.post("/generate")
async def generate_with_api(generate: GenerateData):
    """
    Generate an image using the given GenerateData.

    Parameters:
    - generate (GenerateData): The data used to generate the image.

    Returns:
    - A dictionary containing the generated image filename or an error message.
    """

    start_time = timer()
    images = generate_baby(generate)
    end_time = timer()
    
    total_time = end_time - start_time
    
    json_compatible_item_data = jsonable_encoder({"images": images, "elapsed_time": timedelta(seconds=total_time)})
    return JSONResponse(content = json_compatible_item_data)

@app.post("/generate/emotions")
async def generate_emotion_with_api(data: EmotionData):
    """
    Generate an emotion image using the given EmotionData.

    Parameters:
    - data (EmotionData): The data used to generate the image.

    Returns:
    - A dictionary containing the generated emotion image filename or an error message.
    """

    start_time = timer()
    images = generate_emotions(data)
    end_time = timer()
    
    total_time = end_time - start_time
    
    json_compatible_item_data = jsonable_encoder({"images": images, "elapsed_time": timedelta(seconds=total_time)})
    return JSONResponse(content = json_compatible_item_data)