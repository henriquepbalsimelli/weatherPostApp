import logging
from fastapi import HTTPException
from requests_oauthlib import OAuth1Session
from app.configurations import get_env
import requests

class XSdk:
    def __init__(self) -> None:
        self.__logger = logging.getLogger(__name__)
        self.__consumer_key = get_env('X_API_KEY')
        self.__consumer_secret = get_env('X_API_SECRET_KEY')
        self.__access_token = get_env('X_ACCESS_TOKEN')
        self.__access_token_secret = get_env('X_ACCESS_TOKEN_SECRET')

    def get_auth(self):
        oauth = OAuth1Session(
            self.__consumer_key,
            client_secret=self.__consumer_secret,
            resource_owner_key=self.__access_token,
            resource_owner_secret=self.__access_token_secret
        )
        return oauth

    def __validate_response(self, response: requests.Response):
        if response.status_code not in [200, 201]:
            raise HTTPException(
                status_code=response.status_code,
                detail='X Network error' + response.text
            )
        
    def create_post(self, post_string: str) -> requests.Response:
        try:
            oauth = self.get_auth()

            url = 'https://api.twitter.com/2/tweets'
            payload = {"text": post_string}

            response = oauth.post(url, json=payload)

            self.__validate_response(response=response)

            return response

        except HTTPException as e:
            raise e
        except Exception as e:
            self.__logger.exception(e)
            raise HTTPException(
                status_code=response.status_code,
                detail="Houve um problema para criar postagem no X"
            )