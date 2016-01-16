import redis
import time
unix_timestamp = int(time.time())
r = redis.StrictRedis(host='localhost', port=6379, db=0)

r.lpush('channelmessage_list', *["#LivvTest", '1234message'])
key = 'channelmessage_dict_{unix}'.format(unix=unix_timestamp)
r.hmset(key,
        {
            'channel': '#LivvTest',
            'message': '99999999',
            'sent': False
        },
)

print key
print ''
print r.keys('channelmessage_dict*')
print r.hgetall(key)
