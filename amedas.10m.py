#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
# METADATA
# <xbar.title>amedas</xbar.title>
# <xbar.version>v1.1</xbar.version>
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
import io
import json
import datetime as dt
import tempfile
import base64

import requests
import matplotlib.pyplot as plt
from PIL import Image, ImageOps

# ICON or INFO
MENU_ICON = False

TIMEOUT = 10
WD = '静穏 北北東 北東 東北東 東 東南東 南東 南南東 南 南南西 南西 西南西 西 西北西 北西 北北西 北'.split()
mode = os.environ.get('OS_APPEARANCE', 'Dark')
textcolor = {
    'Light': 'darkslategray',
    'Dark': 'aliceblue',
}[mode]

# VOICEVOX SETTINGS
HOST = '127.0.0.1'
PORT = 50021
ずんだもん = [3, 22]    # 気温
四国めたん = [2, 36]    # 積雪


class AMEDAS:
    def __init__(self):
        self.code = '44132'             # 東京
        self.loc = {}
        self.temp = 100
        self.snow = 0
        self.vvox = True
        self.now = dt.datetime.now(dt.timezone(dt.timedelta(hours=9)))

        # スポット情報取得
        home = os.environ.get('HOME', '.')
        with open(f'{home}/.amedas') as fd:
            self.code = fd.read().strip()
        # 直前の情報を取得
        self.file = f'{home}/.amedas.settings'
        try:
            with open(self.file) as fd:
                self.settings = json.load(fd)
                self.temp = self.settings['temp']
                self.snow = self.settings['snow']
                self.vvox = self.settings['vvox']
        except Exception:
            # 存在しなかったらデフォルトを作成
            self.write_rc()

        self.check_VVOX()
        self.amedas()
        self.write_rc()

    def write_rc(self):
        with open(self.file, 'w') as fd:
            fd.write(json.dumps(
                {
                    'temp': self.temp,
                    'snow': self.snow,
                    'vvox': self.vvox,
                },
                indent=2,
            ))

    def check_VVOX(self, host=HOST, port=PORT):
        if self.vvox:
            try:
                requests.get(
                    f'http://{host}:{port}/docs',
                    timeout=1,
                )
                self.vvox = True
            except Exception:
                self.vvox = False

    def VVOX(self, text, host=HOST, port=PORT, speakers=[3]):
        import pyaudio

        # 声を時間によって使い分ける
        if speakers and isinstance(speakers, list):
            hh = int(self.now.strftime('%H'))
            if hh < 7:
                speaker = speakers[-1]
            else:
                speaker = speakers[0]
        params = {
            'text': text,
            'speaker': speaker,
            'prePhonemeLength': 0,
        }
        query = requests.post(
            f'http://{host}:{port}/audio_query',
            params=params,
        )
        synthesis = requests.post(
            f'http://{host}:{port}/synthesis',
            headers={'Content-Type': 'application/json'},
            params=params,
            data=json.dumps(query.json()),
        )
        voice = synthesis.content

        au = pyaudio.PyAudio()
        stream = au.open(
            format=pyaudio.paInt16,         # 16bit
            channels=1,                     # モノラル
            rate=24000,                     # 設定の「音声のサンプリングレート」に合わせる デフォルトは24000
            output=True,
        )
        stream.write(voice)
        stream.stop_stream()
        stream.close()
        au.terminate()

    def graph(self):
        time_temp = {}
        time_humidity = {}
        time_pressure = {}
        for delta in range(9):
            now = self.now - dt.timedelta(hours=delta * 3) - dt.timedelta(minutes=10)
            yyyymmdd = now.strftime('%Y%m%d')
            HH = now.strftime('%H')
            hh = f'{int(HH) // 3 * 3:02d}'

            # JSONデータのURL
            url = f'https://www.jma.go.jp/bosai/amedas/data/point/{self.code}/{yyyymmdd}_{hh}.json'

            # データを取得
            response = requests.get(url)
            data = response.json()

            # 気圧データと時間データを取得
            for tim in data.keys():
                time_temp[tim] = data[tim]['temp'][0]
                time_humidity[tim] = data[tim]['humidity'][0]
                time_pressure[tim] = data[tim]['pressure'][0]

        time_data = []
        temp_data = []
        humidity_data = []
        pressure_data = []
        for tim in sorted(time_pressure):
            time_data.append(tim)
            temp_data.append(time_temp[tim])
            humidity_data.append(time_humidity[tim])
            pressure_data.append(time_pressure[tim])

        # グラフを描画
        fig, ax = plt.subplots(1, 3, figsize=(3, 1), tight_layout=True)
        ax[0].axis('off')
        ax[0].plot(time_data, temp_data, color='black')
        ax[1].axis('off')
        ax[1].plot(time_data, humidity_data, color='black')
        ax[2].axis('off')
        ax[2].plot(time_data, pressure_data, color='black')

        buf = io.BytesIO()
        fig.savefig(buf, format='PNG')
        plt.close(fig)
        buf.seek(0)
        img = Image.open(buf).convert('RGB')
        img = img.resize((img.width * 30 // img.height, 30))

        _, tmpfile = tempfile.mkstemp()
        img = ImageOps.invert(img)
        img.save(tmpfile, format='PNG')
        with open(tmpfile, 'rb') as fd:
            img_bytes = base64.b64encode(fd.read())
        os.unlink(tmpfile)
        b64img = img_bytes.decode('ascii')

        return b64img

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

        now = self.now - dt.timedelta(minutes=10)
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
                    self.loc.get('kjName', '-') + f' {h}:{m} | color={textcolor}',
                    '---',
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
                        v = _vars[k][0]

                        if k == 'humidity':
                            self.humidity = v
                        if k == 'pressure':
                            self.pressure = v

                        # VOICEVOX ---start
                        if k == 'temp':
                            if int(v) != int(self.temp):
                                pm = ''
                                vv = v
                                if vv < 0:
                                    pm = 'マイナス'
                                    vv = -vv
                                self.temp = v
                                self.VVOX(f'{pm}{vv}度になったのだ', speakers=ずんだもん)
                        if k == 'snow':
                            if int(v) != int(self.snow):
                                self.snow = v
                                self.VVOX(f'{v}センチになったわ', speakers=四国めたん)
                        # VOICEVOX ---end

                        if k == 'windDirection':
                            lines.append(f'{t} {WD[v]} | color={textcolor}')
                        else:
                            if 'snow' not in _vars and k == 'snow1h':
                                continue
                            else:
                                lines.append(f'{t} {v}{u} | color={textcolor}')
                body = '\n'.join(lines)

                if MENU_ICON:
                    print('⛱')
                else:
                    header = [
                        f'{self.temp}C',
                        f'{self.humidity}%',
                        f'{self.pressure}hPa',
                    ]
                    if self.snow:
                        header.append(f'{self.snow}cm')
                    print(' '.join(header) + f' | templateImage={self.graph()}')

                print('---')
                print(body)
                print('---')
                vvoxcolor = 'red' if self.vvox else 'gray'
                print(f'VOICEVOX | color={vvoxcolor} checked={str(self.vvox).lower()}')
        except Exception:
            pass


if __name__ == '__main__':
    AMEDAS()
