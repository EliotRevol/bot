import json

import redis

from gui.src.auth import Auth


def set_passwords(redis_url):
    users = {"user1": json.dumps({'pw': 'pass1'}), "admin": json.dumps({"pw": "passwide"})}
    redis_url.hmset("users", users)


if __name__ == '__main__':
    password = 'passwide'
    url = redis.from_url('redis://default:%s@localhost:6379' % password)
    set_passwords(url)
    print(Auth().check_user_password("admin", "password"))

