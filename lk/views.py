import time

from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.utils.datastructures import SortedDict
import re
import requests
from django.utils.http import urlencode
from lxml import html
from collections import OrderedDict
import urllib2


def home(request):
    template = 'home.html'
    #resp_post_login = requests.post('http://www.lastknights.com/index.php?action=login&ref_id=',
    #                                {'username': 'Livvo', 'password': 'h0nd1!2Ql'})
    #print resp_post_login.status_code
    #print 'Logout found' if resp_post_login.content.find('logout') else 'Not logged in!'




    #cookies = resp_post_login.cookies
    cookies = dict()
    #print cookies['online']
    #print cookies['user']
    print cookies['usercookie1'] if 'usercookie1' in cookies else "No usercookie1"
    print cookies['usercookie2'] if 'usercookie2' in cookies else "No usercookie2"

    cookies['usercookie1'] = 'Livvo'
    cookies['usercookie2'] = '6f295f9a509f539e824cf369cf055207'
    cookies['user'] = 'Livvo%40www.lastknights.com'
    cookies['PHPSESSID'] = 't2jd2261j1lc34gqbnjdpsc0t5'

    resp_get_city_battles = request.get(url='http://www.lastknights.com/index.php?page=battle&sel=city',
                                        cookies=cookies)
    #<a href="index.php?page=battle&amp;battle_id=211146&amp;back=city&amp;sel=city&amp;start=">[Details]</a>
    print(re.findall('[Details]</a>', resp_get_city_battles.content, re.DOTALL))

    resp_get_border = requests.get(url='http://www.lastknights.com/index.php',
                                   params={'loc': 'border'},
                                   cookies=cookies)

    #resp = requests.post('http://www.lastknights.com/index.php?loc=border', {'id': 'Srivijaya', 'type': 'village', 'terrain': 'Forest', 'nr': '5560',
    #                                                                  'attack_now': 'Attack'}, cookies=cookies)

                                   #**dict(allow_redirects=True))
    battle_ids = re.findall('name="terrain" value="Forest".*name="nr" value="(.*?)"', resp_get_border.content, re.DOTALL)
    type_forest = re.findall('name="terrain" value="Forest"', resp_get_border.content, re.DOTALL)
    country_forest = re.findall('name="id" value="(.*?)".*name="terrain" value="Forest"', resp_get_border.content, re.DOTALL)

    print battle_ids, type_forest, country_forest
    return HttpResponse()


    resp_get_camp = requests.get('http://www.lastknights.com/index.php?page=camp', cookies=cookies)

    # Get the time HTML
    # re.findall('<div id="my-time">(.*)</div>', resp_get_camp.content, re.DOTALL)

    # Get the sicklist, infantry, heroes
    # <h3>Sick List [46/46]</h3>
    # Result: ['46/46', ]
    sick_list = re.findall('<h3>Sick List \[(.*?)\]</h3>', resp_get_camp.content, re.DOTALL)
    infantry_list = re.findall('<h3>Infantry \[(.*?)\]</h3>', resp_get_camp.content, re.DOTALL)
    heroes_list = re.findall('<h3>Heroes \[(.*?)\]</h3>', resp_get_camp.content, re.DOTALL)

    resp_get_ranking = requests.get('http://www.lastknights.com/ranking.php?start=1', cookies=cookies)
    points = re.findall('<td><b>(.*?)</b></td>', resp_get_ranking.content, re.MULTILINE)
    names = re.findall('<td>([\w]{3,})?</td>', resp_get_ranking.content, re.DOTALL)
    ranking_names = [x for x in names if x != '']

    reanimation = re.search('<h3>Reanimation(.*)</h3>', resp_get_camp.content)
    td_data = html.fromstring(resp_get_camp.content).xpath('//table[@class="main"]//td/text()')
    # check_pages = SortedDict([
    #     ('logout', resp_post_login.content.find('logout')),
    #     ('encampment_page', resp_get_camp.content.find("Your Military Encampment")),
    #     ('encampment_page_infantry', resp_get_camp.content.find("<h3>Infantry")),
    #     ('encampment_page_infantry_healthy', re.search('<h3>Infantry(.*)</h3>', resp_get_camp.content).groups(1)[0]),
    #     ('encampment_page_infantry_sick', re.search('<h3>Sick(.*)</h3>', resp_get_camp.content).groups(1)[0]),
    #     ('encampment_page_infantry_reanimating', reanimation.groups(1)[0] if reanimation else ''),
    #   ])

    check_pages = SortedDict([
        ('logout', resp_post_login.content.find('logout')),
        ('encampment_page', resp_get_camp.content.find("Your Military Encampment")),
        ('encampment_page_infantry', resp_get_camp.content.find("<h3>Infantry")),
        ('encampment_page_heroes', heroes_list),
        ('encampment_page_infantry_healthy', infantry_list),
        ('encampment_page_infantry_sick', sick_list),
        ('encampment_page_infantry_reanimating', reanimation.groups(1)[0] if reanimation else ''),
        ('ranking', ranking_names),
        ('ranking_with_points', OrderedDict(zip(points, ranking_names))),
    ])

    # import irc

    return render_to_response(template, {
        'check_pages': check_pages,
        'website': get_website()
    }
                              )


def get_website(url=None):
    if not url:
        url = 'http://www.lastknights.com'
    r = requests.get(url)
    return r
