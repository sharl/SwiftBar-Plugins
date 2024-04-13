#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# METADATA
# <xbar.title>disk, memory usage</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Sharl Morlaroll</xbar.author>
# <xbar.author.github>sharl</xbar.author.github>
# <xbar.desc></xbar.desc>
# <xbar.dependencies>python3.11+, psutil, pillow</xbar.dependencies>
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>true</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>true</swiftbar.hideSwiftBar>

import os
import tempfile
import base64

import psutil
from PIL import Image, ImageDraw


def pieUsage(rates, canvas=800, offs=10, hemp=100):
    parts = len(rates)
    img = Image.new('RGBA', (canvas * parts, canvas))
    draw = ImageDraw.Draw(img)

    for i, rate in enumerate(rates):
        start = 270 - 360 * rate
        end = 270

        xy = [
            (offs + canvas * i, hemp),
            (canvas * (i + 1) - offs, canvas - hemp),
        ]
        # 使用率
        draw.pieslice(
            xy,
            start, end,
            fill='Red',
            outline='Red',
            width=1,
        )

    im = img.resize((16 * parts, 16))
    return im


if __name__ == '__main__':
    # disk
    dfs = [df.mountpoint for df in psutil.disk_partitions()]
    s_usage = 0
    v_usage = 0
    for df in dfs:
        if df == '/':
            continue
        du = psutil.disk_usage(df)
        if df.startswith('/System/'):
            s_usage += du.percent
        else:
            v_usage += du.percent
    # memmory
    mem = psutil.virtual_memory()

    rates = [s_usage / 100]
    if v_usage:
        rates.append(v_usage / 100)
    rates.append(mem.percent / 100)
    img = pieUsage(rates, canvas=320, offs=16, hemp=0)

    _, tmpfile = tempfile.mkstemp()
    img.save(tmpfile, format='PNG')
    # base64 encoding
    with open(tmpfile, 'rb') as fd:
        img_bytes = base64.b64encode(fd.read())
    os.unlink(tmpfile)
    b64img = img_bytes.decode('ascii')
    icon = f'| templateImage={b64img}'

    print(icon)
    print('---')

    lines = [f'{s_usage:2.1f}%']
    if v_usage:
        lines.append(f'{v_usage:2.1f}%')
    lines.append(f'{mem.percent:2.1f}%')
    print(' '.join(lines))
