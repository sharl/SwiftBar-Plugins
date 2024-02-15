#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# METADATA
# <xbar.title>札幌 消防出動情報</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Sharl Morlaroll</xbar.author>
# <xbar.author.github>sharl</xbar.author.github>
# <xbar.desc>アメダス地点の最新データを表示します</xbar.desc>
# <xbar.dependencies>python3.11+, requests</xbar.dependencies>
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>true</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>true</swiftbar.hideSwiftBar

import os
import re

import requests

MARK = '🚒'
mode = os.environ.get('OS_APPEARANCE', 'Dark')
textcolor = {
    'Light': 'darkslategray',
    'Dark': 'aliceblue',
}[mode]
URL = 'http://www.119.city.sapporo.jp/saigai/sghp.html'

r = requests.get(URL)
content = r.content.decode('utf-8')
m = re.search(r'(?s)<h2>.*?<h2>', content)
if m:
    match = re.sub(r'<.*?>', '', m[0]).replace('\u3000', '').replace('\r', '')
    lines = []
    for line in match.split('\n'):
        if re.match(r'^・', line):
            lines.append(MARK + line[1:] + f' | color={textcolor} terminal=false bash=open param1={URL}')

    if lines:
        print('\n'.join(lines))
    else:
        print(MARK)
