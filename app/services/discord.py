import requests
import os
import pydash
from configs.token import DISCORD_BOT_TOKEN

class Discord:
    __bot_token = None
    
    def __init__(self, token : str = DISCORD_BOT_TOKEN):
        self.__bot_token = 'Bot {}'.format(token)
        
        pass
    
    def upload(self, channel_id : int, file_paths : list):
        ENDPOINT = "https://discord.com/api/v10/channels/{}/messages".format(channel_id)
        HEADERS = {
            "Authorization": self.__bot_token,
        }
        FILES = []
        for index, file_path in enumerate(file_paths):
            file = open(os.path.abspath(file_path), 'rb')
            FILES.append(("files[{}]".format(index), (file.name, file)))
        
        response = requests.post(ENDPOINT, files = FILES, headers = HEADERS)
        if 200 != response.status_code:
            print("Upload Error : {} - {}".format(response.status_code,response.reason))
            
            return None

        body = response.json()
        attachments = pydash.get(body, 'attachments')
        attachment_urls = pydash.map_(attachments, 'url')
        
        return attachment_urls