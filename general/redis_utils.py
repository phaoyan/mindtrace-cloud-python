import os
import redis

SERVER_HOST = os.getenv('SERVER_HOST')
redis_cli = redis.Redis(host=SERVER_HOST, port=6379, password='$PHYphyPHYphy$')


if __name__ == '__main__':
    print(redis_cli.keys())
