import redis
from irc_client import IrcClient

r = redis.StrictRedis(host='localhost', port=6379, db=0)

irc_client = IrcClient().get_client()

while 1:  # puts it in a loop
    redis_channelmessage_keys = r.keys('channelmessage_dict*')
    if redis_channelmessage_keys:
        for key in redis_channelmessage_keys:
            redis_channelmessage = r.hgetall(key)
            if redis_channelmessage['sent'] == 'False':
                print irc_client.client.send("PRIVMSG {channel} :{message}\n".format(
                        channel=redis_channelmessage['channel'],
                        message=redis_channelmessage['message']
                    )
                )
                #r.hset(key, 'sent', True)
                r.delete(key)