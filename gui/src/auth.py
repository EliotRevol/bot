import json
import os

import redis

ADMIN_USERNAME = 'default'

PORT = '6379'

LOCALHOST = os.environ['REDIS_URL']

PW = 'pw'

ADMIN_PASSWD = 'passwide'  # TODO move to somewhere suitable

USERS = "users"


class Auth:
    """
    Helper class for redis operations
    """

    def __init__(self, ) -> None:
        super().__init__()
        localhost = LOCALHOST
        if localhost is None:
            localhost = "127.0.0.1"
        self.redis = redis.from_url('redis://%s:%s@%s:%s' % (ADMIN_USERNAME, ADMIN_PASSWD, localhost, PORT))
        print("connected redis")

    def check_user_password(self, username, password):
        """
        Checks if given username and password matches with any keys in users scheme
        @:param username
        @:param password
        :return: Boolean flag regarding match
        """
        user_response = self.redis.hget(USERS, username)
        if user_response and json.loads(user_response)[PW] == password:
            return True
        else:
            return False

    def check_user(self, username):
        """
        Checks if username exists in schema
        :param username:
        :return: Boolean flag regarding match
        """
        return username in self.redis.hkeys(USERS)
