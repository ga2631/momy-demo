import io
import os
import base64
import pydash
import uuid
from timeit import default_timer as timer
from datetime import timedelta
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from PIL import Image
from services.face_plus_plus import FacePlusPLus
from services.pixlr_ai import PixlrAI

# import logging
# import logging.config

# config_file = os.path.abspath('configs/logging.conf')
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
    dad_percent: int = 100
    mom_percent: int = 0
    sex: str = 'female'

def save_image(base64_image : str, prefix : str = 'output', is_only_name : bool = False) -> str:
    decoded_bytes = base64.b64decode(base64_image)
    image = Image.open(io.BytesIO(decoded_bytes))

    image_name = prefix + '_' + uuid.uuid4().hex + '.png'
    save_image_path = os.path.abspath(f'static/imgs/generated/{image_name}')
    image.save(save_image_path)
    
    if is_only_name:
        return image_name
    
    return save_image_path

def merge_image(source_file : str, merge_file : str, merge_rate : int = 50) -> str:
    service = FacePlusPLus()

    source_path = os.path.abspath(f'static/imgs/upload/{source_file}')
    merge_path = os.path.abspath(f'static/imgs/upload/{merge_file}')

    base64_image = service.merge_face(source_path = source_path, merge_path = merge_path, merge_rate = merge_rate)
    save_image_path = save_image(base64_image = base64_image)
    
    return save_image_path

def remix(image_path : str = '', sex : str = 'female'):
    PROMPT = f"Transform a person's image into a {sex} 3-month-old baby. Baby is wispy hair, relaxed pose. Baby is smiling. Utilize simple shapes, bold outlines, and limited color palettes. Think of popular flat design illustrations like those used in children's books or mobile apps. Keep the focus on the essential features of the baby"
    NAGATIVE = "Excessive shading, textures, intricate patterns"
    
    service = PixlrAI()
    return service.remix(prompt = PROMPT, negative = NAGATIVE, image_path = image_path)

def generate_baby_with_api(generate: GenerateData):
    source_file = generate.mom
    merge_file = generate.dad
    merge_rate = generate.mom_percent
    
    if 50 < generate.dad_percent:
        source_file = generate.dad
        merge_file = generate.mom
        merge_rate = generate.dad_percent
    
    merge_image_path = merge_image(source_file = source_file, merge_file = merge_file, merge_rate = merge_rate)
    generated_images = remix(image_path = merge_image_path, sex = generate.sex)
    
    paths = []
    for image in generated_images:
        base64_image = pydash.get(image, 'image')
        base64_image = base64_image.replace('data:image/png;base64,', '')
        
        paths.append(save_image(base64_image = base64_image, prefix = 'ai_output', is_only_name = True))
    
    return paths

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
    
    path = os.path.abspath(f'static/imgs/generated/{file_name}')
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
    return {"info": f"file '{file.filename}' saved at '{file_location}'", "filename": filename_tmp}

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
    images = generate_baby_with_api(generate)
    end_time = timer()
    
    total_time = end_time - start_time
    
    json_compatible_item_data = jsonable_encoder({"images": images, "elapsed_time": timedelta(seconds=total_time)})
    return JSONResponse(content = json_compatible_item_data)