#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# METADATA
# <xbar.title>amedas</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Sharl Morlaroll</xbar.author>
# <xbar.author.github>sharl</xbar.author.github>
# <xbar.desc>アメダス地点の最新データを表示します</xbar.desc>
# <xbar.dependencies>python</xbar.dependencies>
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>true</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>true</swiftbar.hideSwiftBar>

import os
import datetime as dt

import requests

TIMEOUT = 10
WD = '静穏 北北東 北東 東北東 東 東南東 南東 南南東 南 南南西 南西 西南西 西 西北西 北西 北北西 北'.split()
mode = os.environ.get('OS_APPEARANCE', 'Dark')
textcolor = {
    'Light': 'darkslategray',
    'Dark': 'aliceblue',
}[mode]


class AMEDAS:
    def __init__(self):
        self.code = '44132'             # 東京
        self.loc = {}

        # スポット情報取得
        home = os.environ.get('HOME', '.')
        with open(f'{home}/.amedas') as fd:
            self.code = fd.read().strip()

        self.amedas()

    def amedas(self):
        try:
            r = requests.get(
                'https://www.jma.go.jp/bosai/amedas/const/amedastable.json',
                timeout=TIMEOUT,
            )
            if r and r.status_code == 200:
                self.loc = r.json()[self.code]
        except Exception:
            pass

        now = dt.datetime.now(dt.timezone(dt.timedelta(hours=9))) - dt.timedelta(minutes=10)
        yyyymmdd = now.strftime('%Y%m%d')
        HH = now.strftime('%H')
        hh = f'{int(HH) // 3 * 3:02d}'
        url = f'https://www.jma.go.jp/bosai/amedas/data/point/{self.code}/{yyyymmdd}_{hh}.json'
        try:
            r = requests.get(url, timeout=TIMEOUT)
            if r and r.status_code == 200:
                data = r.json()
                base_key = f'{yyyymmdd}{HH}0000'        # 積雪は1時間毎
                last_key = list(data.keys())[-1]
                _vars = data[base_key]
                for k in data[last_key]:
                    _vars[k] = data[last_key][k]
                h = last_key[8:10]
                if h == '00':
                    h = '24'
                m = last_key[10:12]
                lines = [
                    self.loc.get('kjName', '-') + f' {h}:{m} | color={textcolor}'
                ]
                for x in [
                        '気温 temp 度',
                        '降水 precipitation1h mm/h',
                        '風向 windDirection -',
                        '風速 wind m/s',
                        '積雪 snow cm',
                        '降雪 snow1h cm/h',
                        '湿度 humidity %',
                        '気圧 pressure hPa',
                ]:
                    t, k, u = x.split()
                    if k in _vars:
                        if k == 'windDirection':
                            lines.append(f'{t} {WD[_vars[k][0]]} | color={textcolor}')
                        else:
                            if 'snow' not in _vars and k == 'snow1h':
                                continue
                            else:
                                lines.append(f'{t} {_vars[k][0]}{u} | color={textcolor}')
                title = '\n'.join(lines)

                print(title)
        except Exception:
            pass


if __name__ == '__main__':
    print('⛱')
    print('---')
    AMEDAS()
