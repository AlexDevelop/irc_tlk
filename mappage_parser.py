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
from lk.models import City, CityToCity

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
    country_city_data = re.findall('<p.*?country=(\w+)".*?/a>(.*?)</p>', str(map_page.content), re.DOTALL)

    if country_city_data:
        current_country = country_city_data[0][0]
        current_country = current_country.strip()
        terrain_type_city = country_city_data[0][1]
        terrain, type_city = terrain_type_city.split(',')
        terrain = terrain.strip()
        type_city = type_city.strip()



    current_city = map_large_page_data[x - 1]

    border_cities_data = re.findall('li.*?country.*?</a>(.*?)</li>', str(map_page.content), re.DOTALL)
    if border_cities_data:
        for city in border_cities_data:
            mps = re.findall('\d', city, re.DOTALL)
            if not mps:
                mps = 1
            else:
                mps = mps[0]
                city = city.replace(' (3mp)', '')
                city = city.replace(' (2mp)', '')
            city = city.replace('.', '')
            city = city.replace(' ', '')
            city = city.replace('-', '')
            current_city = current_city.replace('.', '')
            current_city = current_city.replace(' ', '')
            current_city = current_city.replace('-', '')


            CityToCity.objects.get_or_create(city_name_from=current_city,
                                             city_name_to=city,
                                             mps=int(mps))

    obj, created = City.objects.get_or_create(
            country=current_country,
            city_name=current_city,
            connected_cities=",".join(["".join(xx.replace(" ", "")) for xx in border_cities_data]),
            terrain=terrain, type_city=type_city
    )
    a = 1
    #if x > 30:
    #    exit()
