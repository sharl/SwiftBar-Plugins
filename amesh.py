#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# <xbar.title>アメッシュ</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Sharl Morlaroll</xbar.author>
# <xbar.author.github>sharl</xbar.author.github>
# <xbar.desc>みんな大好き東京アメッシュ</xbar.desc>
# <xbar.image>http://www.hosted-somewhere/pluginimage</xbar.image>
# <xbar.dependencies>python3</xbar.dependencies>
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>true</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>true</swiftbar.hideSwiftBar>

import sys
import io
import time
import datetime

from PIL import Image
import requests

TIMEOUT = 10


BASE_URL = 'https://tokyo-ame.jwa.or.jp'
MAP = BASE_URL + '/map/map000.jpg'
MSK = BASE_URL + '/map/msk000.png'


class AMESH:
    def __init__(self):
        self.img_map = None
        self.img_msk = None
        try:
            r = requests.get(MAP, timeout=TIMEOUT)
            if r and r.status_code == 200:
                self.img_map = Image.open(io.BytesIO(r.content)).convert('RGBA')
            r = requests.get(MSK, timeout=TIMEOUT)
            if r and r.status_code == 200:
                self.img_msk = Image.open(io.BytesIO(r.content)).convert('RGBA')
        except Exception:
            pass

    def getImage(self):
        # round for 5 minutes
        now = time.time() // (5 * 60) * (5 * 60) - (5 * 60)
        jst = datetime.datetime.fromtimestamp(now, datetime.timezone(datetime.timedelta(hours=9)))
        # https://tokyo-ame.jwa.or.jp/mesh/000/201906071525.gif
        rfm = jst.strftime('%Y%m%d%H%M')
        RFM = BASE_URL + f'/mesh/000/{rfm}.gif'

        r = requests.get(RFM, timeout=TIMEOUT)
        if r and r.status_code == 200:
            img_rfm = Image.open(io.BytesIO(r.content)).convert('RGBA')

            img_map = self.img_map.copy()
            img_map.paste(img_rfm, (0, 0), img_rfm)
            img_map.paste(self.img_msk, (0, 0), self.img_msk)
            return img_map


if len(sys.argv) == 1:
    print('⛈')
    print('---')
    print(f'Show | terminal=false bash=\'{sys.argv[0]}\' param1=show')
else:
    if len(sys.argv) > 1 and sys.argv[1] == 'show':
        amesh = AMESH()
        img = amesh.getImage()
        img.show()
