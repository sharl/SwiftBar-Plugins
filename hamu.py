#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# <xbar.title>はむ</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Sharl Morlaroll</xbar.author>
# <xbar.author.github>sharl</xbar.author.github>
# <xbar.desc>いろいろな気象情報を表示します</xbar.desc>
# <xbar.image>http://www.hosted-somewhere/pluginimage</xbar.image>
# <xbar.dependencies>python3</xbar.dependencies>
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>true</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>true</swiftbar.hideSwiftBar>

import os
import sys
import io

from PIL import Image
import requests
from bs4 import BeautifulSoup

TIMEOUT = 10


class AMEHAMU:
    def __init__(self):
        self.base = []

        home = os.environ.get('HOME', '.')
        with open(f'{home}/.location') as fd:
            self.base = fd.read().strip().split('?')

    def getImage(self, mode=''):
        base_url = f'{self.base[0]}{mode}?{self.base[1]}'
        r = requests.get(base_url, timeout=TIMEOUT)
        if r and r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            og_images = soup.find_all('meta', property='og:image')
            if len(og_images) == 0:
                return None
            img_url = og_images[0].get('content')
            r = requests.get(img_url, timeout=TIMEOUT)
            if r and r.status_code == 200:
                return Image.open(io.BytesIO(r.content)).convert('RGB')

        return None

class TenkiJP:
    def __init__(self, mode='気温'):
        print('mode', mode)

        self.mode = mode

    def getImage(self):
        urls = {
            '気温': 'https://tenki.jp/amedas/',
            '降水': 'https://tenki.jp/amedas/precip.html',
            '積雪': 'https://tenki.jp/amedas/snow.html',
        }
        if self.mode in urls:
            r = requests.get(urls[self.mode], timeout=TIMEOUT)
            if r and r.status_code == 200:
                soup = BeautifulSoup(r.content, 'html.parser')
                img = soup.find('img', id='amedas-image')
                img_url = img.get('src')
                r = requests.get(img_url, timeout=TIMEOUT)
                if r and r.status_code == 200:
                    img = Image.open(io.BytesIO(r.content)).convert('RGB')
                    return img

        return None


menus = {
    0: '雨雲',
    1: '雷',
    2: '雨雪',
    3: '気温',
    4: '降水',
    5: '積雪',
    6: '天気図',
    7: '台風',
    8: '台風広域',
}

if len(sys.argv) == 1:
    print('🐹')
    for i in menus.keys():
        if i % 3 == 0:
            print('---')
        print(f'{menus[i]:30s} | terminal=false bash=\'{sys.argv[0]}\' param1={i}')
else:
    menu = int(sys.argv[1])

    if menu >= 0 and menu < 3:
        hamu = AMEHAMU()
        if menu == 0:
            img = hamu.getImage()
        elif menu == 1:
            img = hamu.getImage(mode='lightning')
        else:
            img = hamu.getImage('rainsnow')
        img.show()
    elif menu >= 3 and menu < 6:
        tenkijp = TenkiJP(mode=menus[menu])
        img = tenkijp.getImage()
        img.show()
    elif menu == 6:
        url = 'https://weather.yahoo.co.jp/weather/chart/'
        r = requests.get(url, timeout=TIMEOUT)
        if r and r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            div = soup.find(id='chart-0')
            img_url = div.img['src']
            r = requests.get(img_url, timeout=TIMEOUT)
            if r and r.status_code == 200:
                img = Image.open(io.BytesIO(r.content)).convert('RGB')
                img.show()
    elif menu >= 7 and menu < 9:
        url = 'https://typhoon.yahoo.co.jp/weather/jp/typhoon/'
        typhoons = {
            '台風': url + '?c=1',
            '台風広域': url,
        }
        r = requests.get(url, timeout=TIMEOUT)
        if r and r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            lis = soup.find_all('li', class_='tabView_item')
            for li in lis[2:]:
                typhoons['台風' + li.a.text] = li.a['href']
            typ_url = typhoons[menus[menu]]
            r = requests.get(typ_url, timeout=TIMEOUT)
            if r and r.status_code == 200:
                soup = BeautifulSoup(r.content, 'html.parser')
                div = soup.find('div', class_='tabView_content_image')
                img_url = div.img['src']
                r = requests.get(img_url, timeout=TIMEOUT)
                if r and r.status_code == 200:
                    img = Image.open(io.BytesIO(r.content)).convert('RGB')
                    img.show()
