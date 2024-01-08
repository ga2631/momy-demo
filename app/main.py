import os
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from generate_baby import detect_face, generate_baby_with_api
from fastapi.middleware.cors import CORSMiddleware
import random

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

def build_prompt(generate: GenerateData):
    """
    Generate a prompt for a portrait of a female baby based on the provided generated data.

    Args:
        generate (GenerateData): The generated data object containing the paths to the mom and dad images.

    Returns:
        str: The generated prompt for a portrait of a female baby, which includes the facial features of the dad and mom.
            If the mom or dad image file is not found, an error message is returned instead.
    """
    prompt = '3 month old child, ' + generate.sex + ', smile, Vietnamese people, cartoonize style, portrait, full color, '

    mom_select = []
    if(0 != generate.mom_percent):
        mom_file_location = generate.mom
        if(not os.path.exists(f"static/imgs/{mom_file_location}")):
            return {"error": "mom file not found"}

        mom_detect = detect_face(mom_file_location)
        num_of_resembles = int(len(mom_detect) * generate.mom_percent / 100)
        if 0 == num_of_resembles:
            num_of_resembles = 1
        
        mom_select = random.sample(mom_detect, num_of_resembles)

        print("mom_select:::", ', '.join(mom_select))
        
    dad_select = []
    if(0 != generate.dad_percent):
        dad_file_location = generate.dad
        if(not os.path.exists(f"static/imgs/{dad_file_location}")):
            return {"error": "dad file not found"}

        dad_detect = detect_face(dad_file_location)
        num_of_resembles = int(len(dad_detect) * generate.dad_percent / 100)
        if 0 == num_of_resembles:
            num_of_resembles = 1

        dad_select = random.sample(dad_detect, num_of_resembles)

        print("dad_select:::", ', '.join(dad_select))

    selected = mom_select + dad_select
    unique_selected = set(selected)
    selected_promt = ", ".join(list(unique_selected))

    prompt += selected_promt

    print("finally_prompt:::", prompt)

    return prompt

@app.get("/")
async def root():
    """
        This function is the root endpoint of the API.
        It is an asynchronous function that does not take any parameters.
        It returns a dictionary with a single key-value pair,
        where the key is "message" and the value is "Hello World".
    """
    return {"message": "Hello World"}

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
    file_location = f"static/imgs/{filename_tmp}"

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
    - dict: A dictionary containing the generated image filename or an error message.
    """
    print("Build prompt")
    prompt = build_prompt(generate)
    print("Built")

    print("Generating baby face")
    filename = generate_baby_with_api(prompt)
    print("Generated", filename)
    if(not filename):
        return {"error": "failed to generate image"}

    _path = "static/imgs/" + filename
    return FileResponse(path=_path, media_type="image/png")