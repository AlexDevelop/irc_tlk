import sys
import os
sys.path.append('/home/hvhoek/alex/irc_tlk')

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
import django
django.setup()

from lk.models import City, CityToCity


cities_by_name = {}
cities_formatted = [x for x in City.objects.all()]
cities_to_cities = CityToCity.objects.all()

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

from collections import defaultdict
from heapq import *

def dijkstra(edges, f, t):
    g = defaultdict(list)
    for l,r, c in edges:
        g[l].append((c,r))

    q, seen = [(0,f,())], set()
    while q:
        (cost,v1,path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t:
                return (cost, path)

            for c, v2 in g.get(v1, ()):
                if v2 not in seen:
                    heappush(q, (cost+c, v2, path))

    return float("inf")
c_edges = []

for item in cities_by_name:
    for city in cities_by_name[item]:
        #print(item, city)
        mps = cities_to_cities.filter(city_name_from=item, city_name_to__in=[' ' + city, city])[0].mps
        c_edges.append((item, city, mps))
if __name__ == "__main__":
    edges = [
        ("A", "B", 1),
        ("A", "D", 1),
        ("B", "C", 1),
        ("B", "D", 1),
        ("B", "E", 1),
        ("C", "E", 1),
        ("D", "E", 1),
        ("D", "F", 1),
        ("E", "F", 1),
        ("E", "G", 1),
        ("F", "G", 1)
    ]

    print("=== Dijkstra ===")
    print(c_edges)
    print("A -> G:")
    #print(dijkstra(edges, "A", "G"))
    print(dijkstra(c_edges, "Madrid", "Vorkuta"))




def find_all_paths(graph, start, end, path=[], map_steps=7):
        path = path + [start]
        if end in path:
            return [path]
        if not graph[start]:
            return []
        if len(path) > map_steps:
            return []
        paths = []
        for node in graph[start]:
            if node in path and node is not end:
                continue
            newpaths = find_all_paths(graph, node, end, path, map_steps)
            for newpath in newpaths:
                paths.append(newpath)
        return paths

# routes_dict = {}
# min_val = 123456
# def calculate_mps(route, min_val):
#     length_route = len(route)
#     min_val = min(length_route, min_val)
#     routes_dict.setdefault(length_route, []).append(route)
#     return min_val
#
# routes = find_all_paths(cities_by_name, city_from_name, city_to_name)
# for route in routes:
#     min_val = calculate_mps(route, min_val)
#
# pprint(routes_dict)
# pprint(routes_dict[min_val])