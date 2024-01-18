"""
Pixlr service

Website: https://pixlr.com/image-generator/
Documentation: (Not found)
"""

import os
import requests
import pydash
import time
# import logging
# import logging.config
from configs.token import LEONARDO_AI_TOKEN

# config_file = os.path.abspath('configs/logging.conf')
# logging.config.fileConfig(config_file)
# logger = logging.getLogger('simpleExample')

class LeonardoAI:
    __AUTHORIZATION=LEONARDO_AI_TOKEN

    def __init__(self, token = LEONARDO_AI_TOKEN):
        self.__AUTHORIZATION = f'Bearer {token}'

        pass

    def upload_image(self, image_path : str):
        ENDPOINT = "https://cloud.leonardo.ai/api/rest/v1/init-image"

        HEADERS = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": self.__AUTHORIZATION
        }
        PAYLOAD = {
            "extension": os.path.splitext(image_path)[1].replace('.', ''),
        }
        
        print(PAYLOAD)

        # response = requests.post(ENDPOINT, headers = HEADERS, json=PAYLOAD)

        # print(response.status_code)
        pass
