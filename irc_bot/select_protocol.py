import json
import socket
import select
import time
import re
import collections
from datetime import datetime as dt, timedelta
#from pync import Notifier

import irc_argument_parser as irc_ap
from irc_argument_parser import ArgumentParser, LeaddArgument, SfsArgument
from peewee_db import todos, todos_pvp, Todos_Todolist
from battleparser import BattleParserIrc

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
#import django
#django.setup()

# result_receiving = 'abc !lead add livvo legate'
# found_plugin = [x for x in ArgumentParser().get_subclasses() if x in result_receiving]
# plugin_class = "{}Argument".format(found_plugin.pop().replace('!', '').capitalize())
#
# plugin_class = getattr(irc_ap, plugin_class)
# print(plugin_class('!lead add livvo legate'))
# print(plugin_class('!lead list'))
# print(plugin_class('!lead add livvo legate').data)
# print(plugin_class('!lead list').data)
# exit()
#
def min_max_str(data, length=6, rev=False):
    number = data
    total = length - len(str(number))
    if ' ' in str(number):
        name, number_rev = str(number).split(' ')
    if rev == False:
        return "".join(["".join([" " for x in range(1, total)]), str(number),])
    else:
        if ' ' in str(number):
            total = length - len(name) - len(str(number_rev))
        if ' ' in str(number):
            first_join = [name, "".join([" " for x in range(1, total)]), str(number_rev)]
        else:
            first_join = [number, "".join([" " for x in range(1, total)])]
        return "".join(first_join)
sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock1.connect(('irc.gamesurge.net', 6667))
#sock2.connect(('irc.gamesurge.net', 6667))
connected_sockets = []
channels = ['#DesertAndPlains']  # '#LivvTest', '#LivvTest2', '#DesertAndPlains'
channels = ['#TLK-Dev', '#raberber']  #'#mountainclan']  # '#LivvTest', '#LivvTest2', '#DesertAndPlains'
connected_channels = []
pinged_sockets = []

background_white_color_black = '\x031,0'
background_red_color_white = '\x034,0'
background_end = '\x03'

sfs = False
pvp = False
reminders = []

global flood_protection
flood_protection = []


def check_flood_protection():
    timestamp_now = dt.utcnow().timestamp()
    global flood_protection
    print('FLOOD LEN {}'.format(len(flood_protection)))
    for item in flood_protection:
        if item < (timestamp_now - 12):
            flood_protection.remove(item)
    if len(flood_protection) > 5:
        print('FLOOD', len(flood_protection))
        print(flood_protection[0] < timestamp_now)
        print(flood_protection[0], timestamp_now)
        print((timestamp_now - flood_protection[0]))
        time.sleep(2)
        check_flood_protection()
    if len(flood_protection) > 6:
        print('Waaaait FLOOODING CLOSE!')
        time.sleep(3)

    print('check_flood_protection after checks')

    return True

def send_to_nick(sock, nick, message):
    send_message(sock, nick, message)


def send_to_channel(sock, channel, message):
    if isinstance(channel, list):
        channels = channel
        for channel in channels:
            send_message(sock, channel, message)
    else:
        send_message(sock, channel, message)


def send_message(sock, target, message):
    date_custom = dt.utcnow()
    message = "PRIVMSG {target} :{message}\n".format(target=target, message=message)
    print(message)
    check_flood_protection()
    sock.send(bytes(message, 'ascii'))
    global flood_protection
    flood_protection.append(dt.utcnow().timestamp())


def send_notice(sock, target, message):
    date_custom = dt.utcnow()
    message = "NOTICE {target} :{message} {date}\n".format(target=target, message=message, date=date_custom)
    print(message)
    check_flood_protection()
    sock.send(bytes(message, 'ascii'))
    global flood_protection
    flood_protection.append(dt.utcnow().timestamp())

seconds_running = 0
while 1:
    # Await a read event
    rlist, wlist, elist = select.select([sock1,], [], [], 1)
    # Test for timeout
    if [rlist, wlist, elist] == [[], [], []]:

        #print("Five seconds elapsed.")

        if sock1 not in connected_sockets:
            sock1.send(bytes("NICK BotLivvo\r\n", 'ascii'))
            sock1.send(bytes("USER BotLivvo AAA AAA AAA\r\n", 'ascii'))
            connected_sockets.append(sock1)
            time.sleep(1)

        if sock1 in connected_sockets and sock1 in pinged_sockets and channels != connected_channels and seconds_running > 10:
            diff_channels = [x for x in channels if x not in connected_channels]
            for channel in diff_channels:
                if channel == '#DesertAndPlains':
                    channel = '#DesertAndPlains iguessineedapassword'
                channel_message = 'JOIN {}\n'.format(channel)
                print(channel_message)
                sock1.send(bytes(channel_message, 'ascii'))
                if channel == '#DesertAndPlains iguessineedapassword':
                    channel = '#DesertAndPlains'
                connected_channels.append(channel)

        if sock1 in connected_sockets and sock1 in pinged_sockets and channels == connected_channels and seconds_running > 20:
            if pvp and len(todos_pvp) > 0:
                data = json.loads(todos_pvp[0].data)
                attacker_types = [x for x in json.loads(todos_pvp[0].data)['attacker']]
                attacker_tot = sum([int(json.loads(todos_pvp[0].data)['attacker'][x]['Tot']) for x in attacker_types])
                attacker_inj = sum([int(json.loads(todos_pvp[0].data)['attacker'][x]['Inj']) for x in attacker_types])
                attacker_dead = sum([int(json.loads(todos_pvp[0].data)['attacker'][x]['Dead']) for x in attacker_types])
                attacker_leftover = attacker_tot - attacker_inj - attacker_dead

                defender_types = [x for x in json.loads(todos_pvp[0].data)['defender']]
                defender_tot = sum([int(json.loads(todos_pvp[0].data)['defender'][x]['Tot']) for x in defender_types])
                defender_inj = sum([int(json.loads(todos_pvp[0].data)['defender'][x]['Inj']) for x in defender_types])
                defender_dead = sum([int(json.loads(todos_pvp[0].data)['defender'][x]['Dead']) for x in defender_types])
                defender_leftover = defender_tot - defender_inj - defender_dead

                if attacker_leftover > defender_leftover:
                    outcome = 'Attacker wins'
                elif defender_leftover > attacker_leftover:
                    outcome = 'Defender wins'
                else:
                    outcome = 'Tied'

                battle_time = data['stats']['time'] if 'time' in data['stats'] else 'NO TIME'
                attacker_name = data['stats']['attacker_name']
                outcome_stats = data['stats']['outcome']
                defender_name = data['stats']['defender_name']

                attacker_country = data['stats']['attacker_country']
                defender_country = data['stats']['defender_country']
                attacker_name_stats = data['stats']['attacker_name_stats']

                if outcome_stats == 'defeats':
                    outcome_txt = 'defeats'
                else:
                    outcome_txt = 'loses to'

                todos_pvp[0].status = True
                todos_pvp[0].save()

                country_message = "{bg}{attacker_country} vs {defender_country}{bg_end}: {attacker_name_stats} {outcome_txt} {defender_name}".format(
                        attacker_country=attacker_country, defender_country=defender_country, attacker_name_stats=attacker_name_stats,
                        outcome_txt=outcome_txt, defender_name=defender_name, bg=background_red_color_white, bg_end=background_end)
                send_to_channel(sock1, connected_channels, country_message)

                # Stat: 448 vs 120 soldiers. 448 (100.0%) vs 49 (40.83%) standing. Attacker wins! 11 (22.45%) captured! FLAWLESS!!
                message = "{attacker_name} vs {defender_name}. Stat: {attacker_tot} vs {defender_tot} soldiers. " \
                          "{attacker_leftover} vs {defender_leftover} standing. " \
                          "{outcome}! Time CET (+1): {battle_time}" \
                          "" \
                          "".format(attacker_name=attacker_name, defender_name=defender_name,
                                    attacker_tot=attacker_tot, defender_tot=defender_tot,
                                    attacker_leftover=attacker_leftover, defender_leftover=defender_leftover,
                                    outcome=outcome, battle_time=battle_time)
                send_to_channel(sock1, connected_channels, message)

                todos_pvp = Todos_Todolist.select().where(Todos_Todolist.status == False, Todos_Todolist.todo_type_id == 2).order_by(Todos_Todolist.identifier)

            if sfs and len(todos) > 0:
                data = json.loads(todos[0].data)
                attacker_types = [x for x in json.loads(todos[0].data)['attacker']]
                attacker_tot = sum([int(json.loads(todos[0].data)['attacker'][x]['Tot']) for x in attacker_types])
                attacker_inj = sum([int(json.loads(todos[0].data)['attacker'][x]['Inj']) for x in attacker_types])
                attacker_dead = sum([int(json.loads(todos[0].data)['attacker'][x]['Dead']) for x in attacker_types])
                attacker_leftover = attacker_tot - attacker_inj - attacker_dead

                defender_types = [x for x in json.loads(todos[0].data)['defender']]
                defender_tot = sum([int(json.loads(todos[0].data)['defender'][x]['Tot']) for x in defender_types])
                defender_inj = sum([int(json.loads(todos[0].data)['defender'][x]['Inj']) for x in defender_types])
                defender_dead = sum([int(json.loads(todos[0].data)['defender'][x]['Dead']) for x in defender_types])
                defender_leftover = defender_tot - defender_inj - defender_dead

                data_ext = json.loads(todos[0].data)['attacker']
                data_extf = json.loads(todos[0].data)['defender']

                defenders_count = 0

                if attacker_leftover > defender_leftover:
                    outcome = 'Attacker wins'
                elif defender_leftover > attacker_leftover:
                    outcome = 'Defender wins'
                else:
                    outcome = 'Tied'

                battle_time = data['stats']['time']
                attacker_name = data['stats']['attacker_name']
                outcome_stats = data['stats']['outcome']
                defender_name = data['stats']['defender_name']

                attacker_country = data['stats']['attacker_country']
                defender_country = data['stats']['defender_country']
                attacker_name_stats = data['stats']['attacker_name_stats']

                if defender_tot >= 500:
                    points = "{bg} {points} points gained.{bg_end} ".format(
                            points=int(defender_tot / 4),
                            bg=background_red_color_white, bg_end=background_end
                    )
                else:
                    points = ''

                if outcome_stats == 'defeats':
                    outcome_txt = 'captures'
                else:
                    outcome_txt = 'fails to capture'

                todos[0].status = True
                todos[0].save()

                # 1000
                total_soldiers = attacker_leftover + defender_leftover
                attacker_leftover_perc = round(attacker_leftover / attacker_tot * 100, 2)
                defender_leftover_perc = round(defender_leftover / defender_tot * 100, 2)

                defenders_count = data_extf['Commanders']['Tot']
                country_message = "{bg}{attacker_country} vs {defender_country}{bg_end}: {attacker_name_stats} {outcome_txt} {defender_name} ({defenders_count})".format(
                        attacker_country=attacker_country, defender_country=defender_country, attacker_name_stats=attacker_name_stats,
                        outcome_txt=outcome_txt, defender_name=defender_name, bg=background_white_color_black, bg_end=background_end,
                        defenders_count=defenders_count)
                if attacker_country == 'Berber' or defender_country == 'Berber':
                    send_to_channel(sock1, connected_channels, country_message)

                #if data_extf['Commanders']['Tot'] > 0:
                #    bp = BattleParserIrc(data)
                #    bp.run()
                #    for line in bp.lines:
                #        send_to_channel(sock1, connected_channels, line)

                # Stat: 448 vs 120 soldiers. 448 (100.0%) vs 49 (40.83%) standing. Attacker wins! 11 (22.45%) captured! FLAWLESS!!
                # {attacker_name} vs {defender_name}.
                message = "Stat: {attacker_tot} vs {defender_tot} soldiers. " \
                          "{attacker_leftover} ({attacker_leftover_perc}%) vs {defender_leftover} ({defender_leftover_perc}%) standing. " \
                          "{outcome}! {points}- Time CET (+1): {battle_time}" \
                          "" \
                          "".format(attacker_name=attacker_name, defender_name=defender_name,
                                    attacker_tot=attacker_tot, defender_tot=defender_tot,
                                    attacker_leftover=attacker_leftover, defender_leftover=defender_leftover,
                                    outcome=outcome, battle_time=battle_time, points=points,
                                    defender_leftover_perc=defender_leftover_perc, attacker_leftover_perc=attacker_leftover_perc)

                if attacker_country == 'Berber' or defender_country == 'Berber':
                    send_to_channel(sock1, connected_channels, message)

                if attacker_country == 'Berber':
                    send_notice(sock1, '#LivvTest', 'REJOIN!')
                    #Notifier.notify('REJOIN', title='TLK')

                todos = Todos_Todolist.select().where(Todos_Todolist.status == False, Todos_Todolist.todo_type_id == 1).order_by(Todos_Todolist.identifier)

            if reminders:
                for reminder in reminders:
                    if reminder and dt.utcnow() >= reminder.date_deadline:
                        reminder.status = True
                        reminder.save()
                        message = "{msg} for {nick} - > {desc} ".format(msg='Reminderrrrr', desc=reminder.description, nick=reminder.name)
                        send_to_channel(sock1, reminder.data, message)

        todos = Todos_Todolist.select().where(Todos_Todolist.status == False, Todos_Todolist.todo_type_id == 1).order_by(Todos_Todolist.identifier)
        todos_pvp = Todos_Todolist.select().where(Todos_Todolist.status == False, Todos_Todolist.todo_type_id == 2).order_by(Todos_Todolist.identifier)
        reminders = Todos_Todolist.select().where(Todos_Todolist.status == False, Todos_Todolist.todo_type_id == 3)
    else:
        # Loop through each socket in rlist, read and print the available data
        for sock in rlist:
            try:
                result_receiving = str(sock.recv(1000), 'ascii')
            except UnicodeDecodeError:
                pass
            #print(result_receiving)

            if 'PING :' in result_receiving:
                time.sleep(1)
                message = bytes('PONG {}\r\n'.format(result_receiving.split(':')[1].strip()), 'ascii')
                print(message)
                sock.send(message)
                pinged_sockets.append(sock)

            if 'livvo' in result_receiving:
                print(result_receiving)

            found_plugin = [x for x in ArgumentParser().get_subclasses() if x in result_receiving]
            if found_plugin:
                plugin_class = "{}Argument".format(found_plugin.pop().replace('!', '').capitalize())
                plugin_class = getattr(irc_ap, plugin_class)
                custom_args = result_receiving.split(' :!')[1]
                re_nick = re.findall(':(\w+)!~', result_receiving)
                nick = re_nick.pop() if re_nick else 'Unknown'
                re_channel = re.findall('PRIVMSG (#\w+) :', result_receiving)
                channel = re_channel.pop() if re_channel else 'Unknown'
                extra = {
                    'nick': nick,
                    'channel': channel,  # PRIVMSG #LivvTest :
                }
                data = plugin_class(custom_args, **extra).data
                if data:
                    if isinstance(data, list):
                        for line in data:
                            channel = re.findall('(#[\w-]+) ', result_receiving)
                            send_to_channel(sock, channel[0], line)
                    else:

                        channel = re.findall('(#\w+) ', result_receiving)
                        send_to_channel(sock, channel.pop(), data)

            if '!Livvo' in result_receiving:
                channel = re.findall('(#\w+) ', result_receiving)
                message = '{bg}PONGGG{bg_end}'.format(bg=background_white_color_black, bg_end=background_end)
                send_to_channel(sock, channel.pop(), message)

            if '!sfstats' in result_receiving:
                _, minutes = result_receiving.split('!sfstats')
                minutes = minutes.strip()
                if minutes == '':
                    minutes = 45
                if isinstance(minutes, str):
                    minutes = int(minutes)
                dt_now = dt.utcnow()
                dt_now = dt_now - timedelta(minutes=minutes)
                number_sfs = len(Todos_Todolist.select().where(Todos_Todolist.created >= dt_now, Todos_Todolist.todo_type_id == 1))
                channel = re.findall('(#\w+) ', result_receiving)
                message = '{bg}Number of SF the last {minutes} minutes: {number_sfs}{bg_end}'.format(bg=background_white_color_black, bg_end=background_end, number_sfs=number_sfs, minutes=minutes)

                send_to_channel(sock, channel.pop(), message)

            if '!pvpstats' in result_receiving:
                _, minutes = result_receiving.split('!pvpstats')
                minutes = minutes.strip()
                if minutes == '':
                    minutes = 45
                if isinstance(minutes, str):
                    minutes = int(minutes)
                dt_now = dt.utcnow()
                dt_now = dt_now - timedelta(minutes=minutes)
                pvp_battles = Todos_Todolist.select().where(Todos_Todolist.created >= dt_now, Todos_Todolist.todo_type_id == 2)
                tree = lambda: collections.defaultdict(tree)
                stats = tree()
                for pvp_battle in pvp_battles:
                    data = json.loads(pvp_battle.data)
                    data = data['stats']
                    if 'defeats' in data['outcome']:
                        stats[data['attacker_country']]['wins'] = stats[data['attacker_country']]['wins'] + 1 if 'wins' in stats[data['attacker_country']] else 1
                        stats[data['defender_country']]['losses'] = stats[data['defender_country']]['losses'] + 1 if 'losses' in stats[data['defender_country']] else 1

                    elif 'lost to' in data['outcome']:
                        stats[data['attacker_country']]['losses'] = stats[data['attacker_country']]['losses'] + 1 if 'losses' in stats[data['attacker_country']] else 1
                        stats[data['defender_country']]['wins'] = stats[data['defender_country']]['wins'] + 1 if 'wins' in stats[data['defender_country']] else 1

                    else:
                        stats[data['attacker_country']]['ties'] = stats[data['attacker_country']]['ties'] + 1 if 'ties' in stats[data['attacker_country']] else 1
                        stats[data['defender_country']]['ties'] = stats[data['defender_country']]['ties'] + 1 if 'ties' in stats[data['defender_country']] else 1

                if stats:
                    calc_wins = stats['Berber']['wins']
                    calc_losses = stats['Berber']['losses']
                    calc_add = stats['Berber']['wins'] - stats['Berber']['losses']
                    calc_ties = stats['Berber']['ties'] if 'ties' in stats['Berber'] else 0
                    number_pvps = len(pvp_battles)
                    channel = re.findall('(#\w+) ', result_receiving)
                    message = '{bg}Number of PVPs the last {minutes} minutes: {number_pvps} Wins: {calc_wins} Losses: {calc_losses} Ties: {calc_ties} {bg_end}'.format(
                            bg=background_white_color_black, bg_end=background_end, number_pvps=number_pvps, minutes=minutes,
                        calc_wins=calc_wins, calc_losses=calc_losses, calc_ties=calc_ties
                    )

                    send_to_channel(sock, channel.pop(), message)

            if '!sfs on' in result_receiving:
                sfs = True

            if '!pvp on' in result_receiving:
                pvp = True

            if '!sfs off' in result_receiving:
                sfs = False

            if '!pvp off' in result_receiving:
                pvp = False


    seconds_running += 1


