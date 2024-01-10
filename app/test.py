import io
import os
import base64
import time
import pydash
from PIL import Image
from services.face_plus_plus import FacePlusPLus
from services.pixlr_ai import PixlrAI

def save_image(base64_image : str):
    decoded_bytes = base64.b64decode(base64_image)
    image = Image.open(io.BytesIO(decoded_bytes))

    save_image_path = os.path.abspath('static/imgs/facepp_output_' + time.strftime("%Y%m%d%H%M%S") + '.png')
    image.save(save_image_path)
    
    return save_image_path

def merge_image(source_file : str, merge_file : str) -> str:
    service = FacePlusPLus()

    source_path = os.path.abspath(f'static/imgs/{source_file}')
    merge_path = os.path.abspath(f'static/imgs/{merge_file}')

    base64_image = service.merge_face(source_path=source_path, merge_path=merge_path, merge_rate=50)
    save_image_path = save_image(base64_image)
    
    return save_image_path

def remix(image_path : str = ''):
    PROMPT = "Transform a person's image into a female 3-month-old baby. Baby is wispy hair, relaxed pose. Baby is smiling Utilize simple shapes, bold outlines, and limited color palettes. Think of popular flat design illustrations like those used in children's books or mobile apps. Keep the focus on the essential features of the baby."
    NAGATIVE = "Excessive shading, textures, intricate patterns"
    
    service = PixlrAI()
    return service.remix(prompt = PROMPT, negative = NAGATIVE, image_path = image_path)

source_file = 'z5051735287581_61563fed7ae7e100aeec87606cebddab.jpg'
merge_file = 'z5051735270951_60a7f4087bd6727f1609116a97e6fa8f.jpg'
merge_path = merge_image(source_file, merge_file)
generated_images = remix(image_path = merge_path)

paths = []
for image in generated_images:
    base64_image = pydash.get(image, 'image')
    base64_image = base64_image.replace('data:image/png;base64,', '')
    
    paths.append(save_image(base64_image))

print(paths)