import redis
from dotenv import dotenv_values
config = dotenv_values('.env')


def make():
    return redis.Redis(
        host=config['HOST'],
        port=config['PORT'],
        password=config['PASSWORD'],
        db=0,
        ssl=True,
        ssl_cert_reqs=None)


if __name__ == '__main__':
    r = make()
    # r.flushall()
    print(len(r.keys("TermCounter:*")))
