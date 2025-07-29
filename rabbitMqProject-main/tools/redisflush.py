import redis

def flush_redis():
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.flushdb()

flush_redis()
