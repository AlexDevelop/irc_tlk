import json
from itertools import permutations

import sys

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
from lk.models import City

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

city_from_name = 'Dublin'
city_from = {"from": ('1', 'Dublin'),
             "connected": [["Iceland", " Belfast"], ["England", " Galway"], ["England", " York"], ["England", " Cork"], ["England", " Liverpool"]]}
city_to_name = 'Arendal'

cities = [
    {"from": ('1', 'Dublin'),
     "connected": [["Iceland", " Belfast"], ["England", " Galway"], ["England", " York"], ["England", " Cork"],
                   ["England", " Liverpool"]]},
    {"from": ('2', 'Edinburgh'),
     "connected": [["Muscovy", " Glasgow"], ["Iceland", " Belfast"], ["England", " Durham"]], },
    {"from": ('3', 'Glasgow'), "connected": [["Iceland", " Stornoway"], ["Iceland", " Dundee"], ["Iceland", " Belfast"],
                                             ["Iceland", " Edinburgh"], ["Iceland", " Hofn (2mp)"],
                                             ["Muscovy", " Bergen (2mp)"]], },
    {"from": ('4', 'Belfast'), "connected": [["Muscovy", " Glasgow"], ["Iceland", " Edinburgh"], ["England", " Galway"],
                                             ["England", " Dublin"]], }
]

cities_by_name = {
    'Arendal': ["Malmo", "Bergen", "Gdansk", "Poznan", "Egersund", ],
    'Egersund': ["Arendal", "Dundee", ],
    'Dublin': ["Belfast", "Galway", "York", "Cork","Liverpool", ],
    'Belfast': ["Glasgow", "Edinburgh", "Galway", "Dublin", ],
    'Glasgow': ["Stornoway", "Dundee", "Belfast", "Edinburgh", "Hofn", "Bergen", ],
    'Dundee': ["Glasgow", "Egersund", ],
    'Bergen': ["Arendal", "Glasgow", ],

}
# Dublin, Belfast, Glasgow, Dundee, Egersund, Arendal

def check_city(x, length_max, mp=1, x_counter=0):
    cities_data = []
    cities_data.append(x[0])
    for counter in range(0, length_max + 1):
        try:
            cities_data.append(x[mp + 1])
            if x[mp + 1] in cities_by_name[x[mp]]:
                print('___', x[mp + 1], x[mp], cities_by_name[x[mp]])
                if x[mp + 1] == city_to_name:
                    return mp, cities_data
                #print(x[counter + 1], cities_by_name[x[counter]])
                mp += 1
                x_counter += 1
                return check_city(x, length_max, mp=mp, x_counter=x_counter)
        except:
            pass
    return mp, cities_data

for x in permutations(cities_by_name):
    length_max = len(x) - 1
    if x[0] == city_from_name and x[length_max] == city_to_name:
        check_other_routes = x[2:-1]
        fake_x = []
        fake_x.append(x[0])
        [fake_x.append(x) for x in check_other_routes]
        fake_x.append(x[-1])
        for f_x in permutations(fake_x):
            if f_x[0] == city_from_name and f_x[length_max - 1] == city_to_name:
                response, city_d = check_city(f_x, length_max - 1, mp=0)
                if response >= length_max - 1:
                    pass
                    #print('--', f_x, city_d)
        response, city_d = check_city(x, length_max, mp=0)
        if response >= 3:
            print(x, set(city_d))

exit()
min = 0
max = sys.maxsize
for x in cities_by_name[city_from_name]:
    count = 1
    if x in cities_by_name:
        for z in cities_by_name[x]:
            count += 1
            if z == city_to_name:
                print('VICTORY Route: ', city_from_name, x, z, 'mp:', count)
    continue
    if x[1][0] == 'Glasgow':
        print('------', x[1][0])

    for z in permutations(cities[3]['connected']):
        print('-z--z--z-', x[1][0])
    print(x[1][0])
    print('')
    # print(city)
    # print(city['from'])
    # print(city['connected'])
    # for conn_city in city['connected']:
    #     if conn_city[1] == city_to:
    #         print('Yeaaaah')
    # print('')


exit()

map_large_page = requests.get(url='http://www.lastknights.com/index.php?page=map&sel=&sel=large')
map_large_page_data = re.findall('data-city="(\d+)".*?data-name="(\w+)"', str(map_large_page.content), re.DOTALL)
if map_large_page_data:
    for item in map_large_page_data:
#        print(item)
        pass

for x in range(1, 300):
    map_page = requests.get(url='http://www.lastknights.com/ajax/city_info.php?city_id={}'.format(x))
    #print(dir(map_page))
    #print(map_page.content)
    country_city_data = re.findall('<p.*?country=(\w+)"', str(map_page.content), re.DOTALL)
    if country_city_data:
        current_country = country_city_data[0]
        print(current_country)

    print(map_large_page_data[x - 1], x - 1, '<<')
    border_cities_data = re.findall('li.*?country=(\w+)".*?</a>(.*?)</li>', str(map_page.content), re.DOTALL)
    if border_cities_data:
        for city in border_cities_data:
            print(city)

        print(json.dumps(border_cities_data))

    print(x)
    print(country_city_data[0])
    print(map_large_page_data[x - 1])
    print(City.objects.get_or_create(country=country_city_data[0], city_name=map_large_page_data[x -1], connected_cities=json.dumps(border_cities_data)))
    #if x > 30:
    #    exit()
