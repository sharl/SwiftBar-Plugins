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


def pieUsage(d_rate, m_rate, canvas=800, offs=10, hemp=100):
    img = Image.new('RGBA', (canvas * 2, canvas))
    draw = ImageDraw.Draw(img)

    # disk
    start = 270 - 360 * d_rate
    end = 270

    xy = [
        (offs, hemp),
        (canvas - offs, canvas - hemp),
    ]
    # 使用領域
    draw.pieslice(
        xy,
        start, end,
        fill='Red',
        outline='Red',
        width=10,
    )

    # memory
    start = 270 - 360 * m_rate
    end = 270

    xy = [
        (offs + canvas, hemp),
        (canvas * 2 - offs, canvas - hemp),
    ]
    # 空き領域
    draw.pieslice(
        xy,
        end, start,
        fill='Grey',
        outline='Red',
        width=10,
    )
    im = img.resize((16 * 2, 16))
    return im


if __name__ == '__main__':
    # disk
    dfs = [df.mountpoint for df in psutil.disk_partitions()]
    usage = 0
    for df in dfs:
        if df == '/' or df.startswith('/Volumes'):
            continue
        du = psutil.disk_usage(df)
        usage += du.percent
    # memmory
    mem = psutil.virtual_memory()
    img = pieUsage(usage / 100, mem.percent / 100, canvas=320, offs=2, hemp=0)

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
    print(f'{usage}% {mem.percent}%')
