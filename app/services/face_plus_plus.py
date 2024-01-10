"""
Face++ service

Website: faceplusplus.com
Documentation: https://console.faceplusplus.com/documents/6329700
"""

import os
import requests
import pydash
# import logging
# import logging.config
from configs.token import FACEPLUSPLUS_API_KEY, FACEPLUSPLUS_API_SECRET

# config_file = os.path.abspath('configs/logging.conf')
# logging.config.fileConfig(config_file)
# logger = logging.getLogger('simpleExample')

class FacePlusPLus:
    __API_KEY=FACEPLUSPLUS_API_KEY
    __API_SECRET=FACEPLUSPLUS_API_SECRET

    def __init__(self, api_key = FACEPLUSPLUS_API_KEY, api_secret = FACEPLUSPLUS_API_SECRET):
        self.__API_KEY = api_key
        self.__API_SECRET = api_secret
        pass
    
    def merge_face(self, source_path : str, merge_path : str, merge_rate : int = 50, feature_rate : int = 45) -> dict:
        """
        Merge two faces together using the Face++ API.

        Pricing:
            0.1 USD/Request
            0.0001 USD/Invalid request
            0.0002 USD/Download timeout request

        :param source_path: The path to the source image.
        :type source_path: str
        :param merge_path: The path to the image to merge with the source image.
        :type merge_path: str
        :param merge_rate: The blending rate of the two faces, defaults to 50.
        :type merge_rate: int, optional
        :param feature_rate: The level of facial feature adjustment, defaults to 45.
        :type feature_rate: int, optional

        :return: dict
        """
        
        print('Called Face plus plus. Payload :::: source_path: {}, merge_path: {}, merge_rate: {}, feature_rate: {}'.format(
            source_path,
            merge_path,
            merge_rate,
            feature_rate,
        ))
        # logger.info('Called Face plus plus. Payload :::: source_path: %s, merge_path: %s, merge_rate: %s, feature_rate: %s',
        #     source_path,
        #     merge_path,
        #     merge_rate,
        #     feature_rate,
        # )
        
        ENDPOINT = "https://api-us.faceplusplus.com/imagepp/v1/mergeface"

        source_file = open(source_path, 'rb')
        merge_file = open(merge_path, 'rb')
        FILES = dict({    
            "template_file": source_file,
            "merge_file": merge_file,
        })
        DATA = dict({
            "api_key": self.__API_KEY,
            "api_secret": self.__API_SECRET,
            "merge_rate": merge_rate,
            "feature_rate": feature_rate,
        })
        
        print('Calling Face plus plus API...')
        # logger.debug('Calling API...')
        response = requests.post(ENDPOINT, files=FILES, data=DATA)
        
        if(200 != response.status_code):
            print('Catch error response. Response :::: {}'.format(response.json()))
            # logger.error('Catch error response. Response :::: ' + response.json())
            
            return False

        result = response.json()
        print('Success response\n')
        # logger.info('Success respense.')

        return pydash.get(result, 'result')