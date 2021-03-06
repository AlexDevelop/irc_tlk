import json
import re
import os
import requests
from collections import OrderedDict
from copy import deepcopy
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
from pytz import timezone
import django
from datetime import datetime as dt
import time
import collections

django.setup()

from src import settings

from todos.models import TodoList, TodoType

battle_type_name = OrderedDict()
battle_type_name['Tot'] = 0
battle_type_name['Inj'] = 0
battle_type_name['Dead'] = 0
battle_type_name['Capt'] = 0

attacker_stats = OrderedDict()
attacker_stats['Commanders'] = deepcopy(battle_type_name)
attacker_stats['Heroes'] = deepcopy(battle_type_name)
attacker_stats['Artillery'] = deepcopy(battle_type_name)
attacker_stats['Cavalry'] = deepcopy(battle_type_name)
attacker_stats['Infantry'] = deepcopy(battle_type_name)

defender_stats = OrderedDict()
defender_stats['Commanders'] = deepcopy(battle_type_name)
defender_stats['Heroes'] = deepcopy(battle_type_name)
defender_stats['Artillery'] = deepcopy(battle_type_name)
defender_stats['Cavalry'] = deepcopy(battle_type_name)
defender_stats['Infantry'] = deepcopy(battle_type_name)


cookies = dict()
cookies['usercookie1'] = 'Livvo'
cookies['usercookie2'] = '6f295f9a509f539e824cf369cf055207'
cookies['user'] = 'Livvo%40www.lastknights.com'
cookies['PHPSESSID'] = 't2jd2261j1lc34gqbnjdpsc0t5'

while True:
    print('{} Sleeping for 2'.format(dt.utcnow()))
    time.sleep(2)
    resp_get_city_battles = requests.get(url='http://www.lastknights.com/index.php?page=battle&sel=pvp',
                                    cookies=cookies)

    battles_list = re.findall('a href="index.php\?page=battle&amp;battle_id=(\d*)&amp;back=pvp&amp;sel=pvp&amp;start=', str(resp_get_city_battles.content), re.DOTALL)
    if not battles_list:
        continue
    battles_list = re.findall('tr class="(?:even|odd)".*?class="flag symbol" title="(\w*)".*?<td>(.*?)</td>.*?color="(?:red|lime)">.*?(loses|defeats).*?</font.*?class="flag symbol" title="(\w*)".*?span title="(.*?)" >.*?</span>.*?a href="index.php\?page=battle&amp;battle_id=([\d\;&]*)&amp;back=pvp&amp;sel=pvp&amp;start=', str(resp_get_city_battles.content), re.DOTALL)
    battles_list.sort(reverse=True)
    battles_list = {int(battle_id): {'attacker_country':a, 'attacker_name_stats':b, 'outcome': c, 'defender_country':d, 'time': e} for (a,b,c,d,e, battle_id) in battles_list}
    battles_list = collections.OrderedDict(sorted(battles_list.items(), reverse=True))

    if battles_list:

        tlk_type = TodoType.objects.get(group='TLKPVP')
        existing_battles = [int(x) for x in TodoList.objects.filter(todo_type=tlk_type).values_list('identifier', flat=True)]
        # [x for x in existing_battles if x not in [int(x) for x in TodoList.objects.filter(todo_type=tlk_type).values_list('identifier', flat=True)]]
        new_battle_list = [int(x) for x in battles_list if int(x) not in existing_battles]
        for battle_id in new_battle_list:
        #for battle_id, battle_stats in battles_list.iteritems():
            battle_stats = battles_list[battle_id]
            print('Found new battle {id}'.format(id=battle_id))

            resp_get_city_battle_latest = requests.get(
                    url='http://www.lastknights.com/index.php?page=battle&battle_id={}&back=pvp&sel=pvp&start='.format(battle_id),
                    cookies=cookies
            )

            city_battle_stats = re.findall('<table width="100%">(.*?)</table>', str(resp_get_city_battle_latest.content), re.DOTALL)
            attacker_name, outcome, defender_name = re.findall('<font size="4">(.*?)</font>', city_battle_stats[1], re.DOTALL)
            city_battle_stats_tr = re.findall('<td>(.*?)</td>', city_battle_stats.pop(), re.DOTALL)
            #print city_battle_stats
            # print city_battle_stats_tr
            side = 'attacker'
            count = 0
            for item in city_battle_stats_tr:
                if 'font size' in item:
                    continue
                data_stats = globals()['{}_stats'.format(side)]

                if count == 0:
                    unit_type = item

                if item == '--':
                    item = 0

                # print side, unit_type, item, count

                if count == 1:
                    globals()['{}_stats'.format(side)][unit_type]['Tot'] = int(item)
                if count == 2:
                    globals()['{}_stats'.format(side)][unit_type]['Inj'] = int(item)
                if count == 3:
                    globals()['{}_stats'.format(side)][unit_type]['Dead'] = int(item)
                if count == 4:
                    globals()['{}_stats'.format(side)][unit_type]['Capt'] = int(item)

                count += 1

                if item == '' or (count == 5 and side == 'defender'):
                    if side == 'attacker':
                        side = 'defender'
                    else:
                        side = 'attacker'

                    count = 0

            tz_custom = timezone('Europe/Amsterdam')
            try:
                dt_time = tz_custom.localize(dt.strptime(battle_stats['time'], '%A %B %dth %Y, %H:%M'))
            except ValueError:
                pass

            try:
                dt_time = tz_custom.localize(dt.strptime(battle_stats['time'], '%A %B %dst %Y, %H:%M'))
            except ValueError:
                pass

            try:
                dt_time = tz_custom.localize(dt.strptime(battle_stats['time'], '%A %B %dnd %Y, %H:%M'))
            except ValueError:
                pass

            try:
                dt_time = tz_custom.localize(dt.strptime(battle_stats['time'], '%A %B %drd %Y, %H:%M'))
            except ValueError:
                pass


            default_tlk = {
                'created': dt_time,
                'todo_type': TodoType.objects.get(group='TLKPVP'),
                'date_deadline': dt.now().replace(year=2100, month=1, day=1, hour=0, minute=0, microsecond=0,
                                                  tzinfo=timezone('Europe/Amsterdam'))
            }
            todolist_item, created = TodoList.objects.get_or_create(identifier=battle_id, defaults=default_tlk)
            todolist_item.data = json.dumps(
                    {
                        'attacker': attacker_stats,
                        'defender': defender_stats,
                        'stats': {
                            'attacker_name': attacker_name,
                            'attacker_country': battle_stats['attacker_country'],
                            'attacker_name_stats': battle_stats['attacker_name_stats'],
                            'outcome': outcome,
                            'defender_name': defender_name,
                            'defender_country': battle_stats['defender_country'],
                            'time': battle_stats['time'],
                        }
                    }
            )
            todolist_item.identifier = battle_id
            todolist_item.created = dt_time
            todolist_item.save()
