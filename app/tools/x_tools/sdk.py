import logging
from fastapi import HTTPException
from app.configurations import get_env
import tweepy
from tweepy.errors import HTTPException as TweepyHTTPException

class XSdk:
    def __init__(self) -> None:
        self.__logger = logging.getLogger(__name__)
        self.__consumer_key = get_env('X_API_KEY')
        self.__consumer_secret = get_env('X_API_SECRET_KEY')
        self.__access_token = get_env('X_ACCESS_TOKEN')
        self.__access_token_secret = get_env('X_ACCESS_TOKEN_SECRET')

    def get_auth(self) -> tweepy.Client:
        client = tweepy.Client(
            consumer_key=self.__consumer_key,
            consumer_secret=self.__consumer_secret,
            access_token=self.__access_token,
            access_token_secret=self.__access_token_secret
        )
        return client
        
    def create_post(self, post_string: str) -> tweepy.Response:
        try:
            client = self.get_auth()

            response = client.create_tweet(text=post_string)

            return response

        except TweepyHTTPException as e:
            raise e
        except Exception as e:
            self.__logger.exception(e)
            raise HTTPException(
                status_code=500,
                detail="Houve um problema para criar postagem no X"
            )