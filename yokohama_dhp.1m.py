#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# METADATA
# <xbar.title>横浜 消防出動情報</xbar.title>
# <xbar.version>v1.2</xbar.version>
# <xbar.author>Sharl Morlaroll</xbar.author>
# <xbar.author.github>sharl</xbar.author.github>
# <xbar.desc></xbar.desc>
# <xbar.dependencies>python3.11+, requests</xbar.dependencies>
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>true</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>true</swiftbar.hideSwiftBar>

import os
import re

import requests

MARK = '🚒'
mode = os.environ.get('OS_APPEARANCE', 'Dark')
textcolor = {
    'Light': 'darkslategray',
    'Dark': 'aliceblue',
}[mode]
URL = 'https://cgi.city.yokohama.lg.jp/shobo/disaster/'

r = requests.get(URL)
content = r.content.decode('utf-8')
m = re.search(r'(?s)<font size=2 color=black >.*?<hr.*?>', content)
if m:
    match = re.sub(r'で発生した.*?に、.*?等が出場しています。', '', re.sub(r'<.*?>', '', m[0]).replace('\u3000', '').replace('\r', ''))
    lines = []
    for line in match.split('\n'):
        if line and line != 'こちらは横浜市消防局です。ただいま市内に火災等は発生しておりません。':
            lines.append(MARK + line + f' | color={textcolor} terminal=false bash=open param1={URL}')

    if lines:
        print('\n'.join(lines))
