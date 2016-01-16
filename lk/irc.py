import socket
import sys
import redis
import time
import json
from irc_client import IrcClient


r = redis.StrictRedis(host='localhost', port=6379, db=0)

# IRC Settings
server = "irc.gamesurge.net"  # settings
channel = "#LivvTest"
botnick = "LivvBot"

import random

print random.randrange(0, 10)

irc_client = IrcClient().check_client()
print "connecting to:" + server
irc_client.connect_response = irc_client.client.connect((server, 6667))  # connects to the server
irc_client.client.send("USER " + botnick + " " + botnick + " " + botnick + " :This is a fun bot!\n")  # user authentication
irc_client.client.send("QUOTE PONG 395620065\n")  # sets nick
irc_client.client.send("NICK " + botnick + "\n")  # sets nick
# irc.send("PRIVMSG Livvo :iNOOPE\r\n")    #auth
# irc.send("JOIN "+ channel +" Livv\n")        #join the chan


def sleep(seconds=2):
    print 'sleeping for {seconds}'.format(seconds=seconds)
    time.sleep(seconds)

random_text = [
    'aaaa',
    'bbbb',
    'cccc'
]

count = 0
first_pong = False
while 1:  # puts it in a loop
    text = irc_client.client.recv(2040)  # receive the text
    text_output = "-- {}".format(text)
    if text_output == '-- ':
        sleep()
    print text_output  # print text to console

    if text.find('PING') != -1:  # check if 'PING' is found
        print irc_client.client.send('PONG ' + text.split()[1] + '\r\n')
        first_pong = True
        sleep(2)
        irc_client.client.send("JOIN " + channel + " Livv\n")  # join the chan
        sleep(2)
        irc_client.client.send("PRIVMSG {channel} :{message}\n".format(channel=channel, message="if emptyyy"))
        sleep(2)

    if first_pong and count == 0:
        print 'First Pong True'
        print irc_client.client.send("PRIVMSG {channel} :{message}\n".format(channel=channel, message="Test Alex"))
        count += 1

    # redis_channelmessage = r.hgetall('channelmessage_dict')
    # redis_channelmessage_keys = r.keys('channelmessage_dict*')
    # if first_pong and redis_channelmessage_keys:
    #     for key in redis_channelmessage_keys:
    #         redis_channelmessage = r.hgetall(key)
    #         if redis_channelmessage['sent'] == 'False':
    #             print irc_client.client.send("PRIVMSG {channel} :{message}\n".format(
    #                     channel=redis_channelmessage['channel'],
    #                     message=redis_channelmessage['message']
    #                 )
    #             )
    #             #r.hset(key, 'sent', True)
    #             r.delete(key)

    #
    # elif text.find(':To connect') != -1:  #
    #     irc.send('PONG ' + text.split()[1] + '\r\n')
    #     time.sleep(2)
    #     irc.send("JOIN " + channel + " Livv\n")  # join the chan
    #     time.sleep(2)
    #     irc.send("PRIVMSG {channel} :{message}\n".format(channel=channel, message="elif emptyyy"))
    #     time.sleep(2)

    # else:
    #     time.sleep(2)
    #     irc.send("JOIN " + channel + " Livv\n")  # join the chan
    #     time.sleep(2)
    #     irc.send("PRIVMSG {channel} :{message}\n".format(channel=channel, message="else emptyyy"))

    # if random.randrange(0, 2) == 1:
    #     time.sleep(2)
    #     print 'yaarrrrr'
    #     if len(random_text) > 0:
    #         text = random_text.pop(0)
    #         print "PRIVMSG {channel} :{message}".format(channel=channel, message=text)
    #         irc.send("PRIVMSG {channel} :{message}\n".format(channel=channel, message=text))
    #     else:
    #         print "PRIVMSG {channel} :{message}".format(channel=channel, message='emptyyy')
    #         irc.send("PRIVMSG {channel} :{message}\n".format(channel=channel, message="emptyyy"))
    #
    # time.sleep(2)
