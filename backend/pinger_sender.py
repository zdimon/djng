import socketio
import json
import sys
import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)


while True:
    data = {'task': 'gather_active_connections'}
    redis_client.publish('notifications', json.dumps(data))
    import time
    time.sleep(5)