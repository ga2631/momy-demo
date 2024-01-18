"""
Pixlr service

Website: https://pixlr.com/image-generator/
Documentation: (Not found)
"""

import os
import requests
import pydash
# import logging
# import logging.config
from configs.token import PIXLR_CLIENT_KEY, PIXLR_CLIENT_SECRET

# config_file = os.path.abspath('configs/logging.conf')
# logging.config.fileConfig(config_file)
# logger = logging.getLogger('simpleExample')

class PixlrAI:
    __CLIENT_KEY=PIXLR_CLIENT_KEY
    __CLIENT_SECRET=PIXLR_CLIENT_SECRET

    def __init__(self, client_key = PIXLR_CLIENT_KEY, client_secret = PIXLR_CLIENT_SECRET):
        self.__CLIENT_KEY = client_key
        self.__CLIENT_SECRET = client_secret
        pass

    def remix(self, prompt : str, negative : str = '', image_path : str = '', influence : int = 50, width : int = 1024, height : int = 1024, amount : int = 4) -> list:
        """
        Remixes an image using the Pixlr API.
        
        Pricing:
            (https://pixlr.com/pricing)
            Plus: 1.99$/80 Credits/month. Unlimited saves. 0.99$/month (~11.88$) for yearly
            *Premium*: 7.99$/1000 Credits/month. Unlimited saves, Private mode for AI Generations, elements, animations and more. 4.90$/month (~58.8$) for yearly 
            Team: 12.99$/5 Premium seats. 1000 Credits/seat/month. 9.91$/month (~118.92$) for yearly 
            
            1 credit ~ 1 images

        Parameters:
            prompt (str): The prompt for the remix.
            negative (str): The negative for the remix. Default is an empty string.
            image_path (str): The path to the image file. Default is an empty string.
            influence (int): The level of influence for the remix. Default is 50.
            width (int): The width of the image. Default is 1024.
            height (int): The height of the image. Default is 1024.
            amount (int): The amount of remixes to generate. Default is 4.

        Returns:
            list: The image data of the remix.
        """
        
        print('Called PixlrAI. Payload :::: prompt: {}; negative: {}; image_path: {}; influence: {}; width: {}; height: {}; amount: {}'.format(
            prompt,
            negative,
            image_path,
            influence,
            width,
            height,
            amount
        ))
        # logger.info('Called PixlrAI. Payload :::: prompt: %s, negative: %s, image_path: %s, influence: %s, width: %s, height: %s, amount: %s ',
        #     prompt,
        #     negative,
        #     image_path,
        #     influence,
        #     width,
        #     height,
        #     amount,
        # )
        
        ENDPOINT = "https://pixlr.com/api/openai/remix"

        FILES = ''
        _image_path = os.path.abspath(image_path)
        if os.path.exists(_image_path):
            image_file = open(_image_path, 'rb')
            FILES = dict({
                "image": image_file,
            })
        
        DATA = dict({
            "prompt": prompt,
            "negative": negative,
            "personal": False,
            "influence": influence,
            "amount": amount,
            "width": width,
            "height": height,
        })
        
        print('Calling Pixlr API...')
        # logger.debug('Calling API...')
        try:
            response = requests.post(ENDPOINT, files=FILES, data=DATA)
        except NameError:
            print(NameError)

            return False
            
        print(response)
        
        if(200 != response.status_code):
            print('Catch error response. Response :::: {}'.format(response.json()))
            # logger.error('Catch error response. Response :::: ' + response.json())
            
            return False

        result = response.json()
        print('Success response\n')
        # logger.info('Success respense.')

        return list(pydash.get(result, 'data.images'))