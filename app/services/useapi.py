import time
import midjourney_api_client
from typing import Union
from configs.token import USEAPI_TOKEN, USEAPI_DISCORD, USEAPI_SERVER, USEAPI_CHANNEL, USEAPI_CALLBACK
from midjourney_api_client.api.default_api import DefaultApi
from midjourney_api_client.models.describe_response import DescribeResponse
from midjourney_api_client.models.imagine_response import ImagineResponse
from midjourney_api_client.models.job_response import JobResponse
from midjourney_api_client.models.jobs_blend_post_request import JobsBlendPostRequest
from midjourney_api_client.models.jobs_button_post_request import JobsButtonPostRequest
from midjourney_api_client.models.jobs_describe_post_request import JobsDescribePostRequest
from midjourney_api_client.models.jobs_imagine_post_request import JobsImaginePostRequest
from midjourney_api_client.rest import ApiException

class UseApi:
    __api_token = USEAPI_TOKEN
    __discord = USEAPI_DISCORD
    __server = USEAPI_SERVER
    __channel = USEAPI_CHANNEL
    __reply_url = USEAPI_CALLBACK
    
    __configuration = None
    
    __time_sleep = 5
    
    def __init__(self, token = USEAPI_TOKEN, discord = USEAPI_DISCORD, server = USEAPI_SERVER, channel = USEAPI_CHANNEL, callback = USEAPI_CALLBACK):
        self.__api_token = token
        self.__discord = discord
        self.__server = server
        self.__channel = channel
        self.__reply_url = callback
        
        self.__configuration = midjourney_api_client.Configuration(
            host = "https://api.useapi.net/v1",
            access_token = self.__api_token
        )
        
        pass
    
    def __wait_for_job_to_complete(self, api_instance: DefaultApi, job: Union[DescribeResponse, ImagineResponse, JobResponse]):
        verb = job.verb.upper()
        print(f"{verb} : {job.status}", job.jobid)

        while job.code == 200 and job.status in ['started', 'progress']:
            # Sleep for 20 seconds
            time.sleep(self.__time_sleep)  
            job = api_instance.jobs_get(job.jobid)
            print(f"{verb} : {job.status}", {"jobid": job.jobid, "content": job.content})

        if isinstance(job, JobResponse) and job.attachments:
            print(f"{verb} url", job.attachments[0].url)
        if isinstance(job, JobResponse) and job.buttons:
            print(f"{verb} buttons", ", ".join(job.buttons))

        return job
    
    def describe(self):
        with midjourney_api_client.ApiClient(self.__configuration) as api_client:
            # Create an instance of the API class
            api_instance = midjourney_api_client.DefaultApi(api_client)

            # Midjourney /describe
            try:
                jobs_describe_post_request = JobsDescribePostRequest(
                    describeUrl="https://mymodernmet.com/wp/wp-content/uploads/2017/12/free-images-national-gallery-of-art-9.jpg",
                    discord=self.__discord,
                    server=self.__server,
                    channel=self.__channel,
                    reply_url=self.__reply_url
                )
                describe_response = api_instance.jobs_describe_post(jobs_describe_post_request)
                describe_response = self.__wait_for_job_to_complete(api_instance = api_instance, job = describe_response)

                return describe_response
            
            except ApiException as e:
                print("Exception when calling jobs_describe_post_request: %s\n" % e)
        
    def blend(self):
        with midjourney_api_client.ApiClient(self.__configuration) as api_client:
            # Create an instance of the API class
            api_instance = midjourney_api_client.DefaultApi(api_client)
                
            # Midjourney /blend
            try:
                jobs_blend_post_request = JobsBlendPostRequest(
                    blendUrls = [
                        "https://mymodernmet.com/wp/wp-content/uploads/2017/12/free-images-national-gallery-of-art-6.jpg",
                        "https://mymodernmet.com/wp/wp-content/uploads/2017/12/free-images-national-gallery-of-art-2.jpg"
                    ],
                    discord=self.__discord,
                    server=self.__server,
                    channel=self.__channel,
                    reply_url=self.__reply_url
                )
                blend_response = api_instance.jobs_blend_post(jobs_blend_post_request)
                blend_response = self.__wait_for_job_to_complete(api_instance = api_instance, job = blend_response)

                return blend_response
            
            except ApiException as e:
                print("Exception when calling jobs_blend_post: %s\n" % e)
                
    def imagine(self, prompt):
        with midjourney_api_client.ApiClient(self.__configuration) as api_client:
            # Create an instance of the API class
            api_instance = midjourney_api_client.DefaultApi(api_client)
            
            # Midjourney /imagine
            try:
                jobs_imagine_post_request = JobsImaginePostRequest(
                    prompt=prompt,
                    discord=self.__discord,
                    server=self.__server,
                    channel=self.__channel,
                    reply_url=self.__reply_url
                )
                imagine_response = api_instance.jobs_imagine_post(jobs_imagine_post_request)
                imagine_response = self.__wait_for_job_to_complete(api_instance = api_instance, job = imagine_response)
                
                return imagine_response

            except ApiException as e:
                print("Exception when calling jobs_imagine_post: %s\n" % e)