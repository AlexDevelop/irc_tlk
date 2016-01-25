import json
from itertools import permutations, combinations

import sys
from pprint import pprint

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

# cities_by_name = {
#     'Arendal': ["Malmo", "Bergen", "Gdansk", "Poznan", "Egersund", ],
#     'Egersund': ["Arendal", "Dundee", ],
#     'Dublin': ["Belfast", "Galway", "York", "Cork","Liverpool", ],
#     'Belfast': ["Glasgow", "Edinburgh", "Galway", "Dublin", ],
#     'Glasgow': ["Stornoway", "Dundee", "Belfast", "Edinburgh", "Hofn", "Bergen", ],
#     'Dundee': ["Glasgow", "Egersund", ],
#     'Bergen': ["Arendal", "Glasgow", ],
#     'Mo': ["Narvik", "Jokkmokk", ],
# }
cities_by_name = {}
cities_formatted = [x for x in City.objects.all()]
for city in cities_formatted:
    city_name = city.city_name.replace('(3mp)', '')
    city_name = city_name.replace('-', '')
    city_name = city_name.replace('(2mp)', '')
    city_name = city_name.replace('.', '')
    city_name = city_name.replace(' ', '')
    connected_cities = city.connected_cities.split(',')
    connected_cities = [x.replace('.', '') for x in [x.replace('(3mp)', '') for x in connected_cities]]
    connected_cities = [x.replace('(2mp)', '') for x in connected_cities]
    connected_cities = [x.replace('-', '') for x in connected_cities]
    connected_cities = [x.replace(' ', '') for x in connected_cities]
    cities_by_name[city_name] = connected_cities


def check_connected_cities(cities):
    length_cities = len(cities)
    data = []
    for counter in range(0, length_cities - 1):
        if cities[counter] in cities_by_name and cities[counter + 1] in cities_by_name[cities[counter]]:
            if cities[counter] not in data:
                data.append(cities[counter])
            if cities[counter + 1] not in data:
                data.append(cities[counter + 1])
        else:
            return False

    return len(data) == length_cities


def check_order_cities(cities):
    length_cities = len(cities)
    for counter in range(0, length_cities - 1):
        if cities[counter] in cities_by_name and not cities[counter + 1] in cities_by_name[cities[counter]]:
            return False

    return True


def check_from_to_cities(cities):
    if cities[0] != city_from_name:
        return False
    if cities[-1] != city_to_name:
        return False

    return True


def _myloop(data=[], count=0):
    data.append(count)
    count += 1

    if count >= 10:
        return data
    return _myloop(data, count)

found_items = []
mps = {
    '2': [],
    '3': [],
    '4': [],
    '5': [],
    '6': [],
}
for city in cities_by_name[city_from_name]:
    for item_a in permutations(cities_by_name[city]):
        for city_a in item_a:

            for item_b in permutations(cities_by_name[city_a]):
                for city_b in item_b:

                    for city_c in cities_by_name[city_b]:

                        for item_d in cities_by_name[city_c]:
                            if item_d in cities_by_name:
                                # if item_d or city_c or city_b in data:
                                #     continue
                                for city_e in cities_by_name[item_d]:
                                    if city_e in cities_by_name and city_to_name in cities_by_name[city_e]:
                                        data = ['d', city_from_name, city, city_a, city_b, city_c, item_d, city_e, city_to_name]
                                        if [len(data), data] not in found_items:
                                            found_items.append(([len(data), data]))

                        if city_to_name in cities_by_name[city_c]:
                            data = [city_from_name, city, city_a, city_b, city_c, city_to_name]
                            if [len(data), data] not in found_items:
                                found_items.append(([len(data), data]))

                    if city_to_name in cities_by_name[city_b]:
                        data = [city_from_name, city, city_a, city_b, city_to_name]
                        if [len(data), data] not in found_items:
                            found_items.append(([len(data), data]))
                            #print('aaa', data)

                if city_to_name in cities_by_name[city_a]:
                    data = [city_from_name, city, city_a, city_to_name]
                    found_items.append([len(data), data])

for item in found_items:
    if item[0] == 3:
        mps[str(item[0])].append(item[1])
    if item[0] == 4:
        mps[str(item[0])].append(item[1])
    if item[0] == 5:
        mps[str(item[0])].append(item[1])
    if item[0] == 6:
        mps[str(item[0])].append(item[1])

pprint(found_items, width=150)
pprint(mps, width=150)



#pprint(_myloop())
#print(_myloop())
exit()

map_large_page = requests.get(url='http://www.lastknights.com/index.php?page=map&sel=&sel=large')
map_large_page_data = re.findall('data-city.*?data-name="(.*?)"', str(map_large_page.content), re.DOTALL)
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

    border_cities_data = re.findall('li.*?country.*?</a>(.*?)</li>', str(map_page.content), re.DOTALL)
    if border_cities_data:
        for city in border_cities_data:
            pass

    obj, created = City.objects.get_or_create(country=country_city_data[0], city_name=map_large_page_data[x - 1], connected_cities=",".join(["".join(xx.replace(" ", "")) for xx in border_cities_data]))
    a = 1
    #if x > 30:
    #    exit()
