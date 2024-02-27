#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# METADATA
# <xbar.title>diskfree</xbar.title>
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


def pieDiskUsage(rate, canvas=800, offs=10, hemp=100):
    start = 270 - 360 * rate
    end = 270

    xy = [
        (offs, hemp),
        (canvas - offs, canvas - hemp),
    ]

    img = Image.new('RGBA', (canvas, canvas))
    draw = ImageDraw.Draw(img)

    # 使用領域
    draw.pieslice(
        xy,
        start, end,
        fill='Red',
        outline='Red',
        width=10,
    )
    # 空き領域
    # draw.pieslice(
    #     xy,
    #     end, start,
    #     fill='Grey',
    #     outline='Red',
    #     width=10,
    # )
    im = img.resize((16, 16))
    return im


if __name__ == '__main__':
    dfs = [df.mountpoint for df in psutil.disk_partitions()]

    usage = 0
    for df in dfs:
        if df == '/':
            continue
        du = psutil.disk_usage(df)
        usage += du.percent
    img = pieDiskUsage(usage / 100, canvas=320, offs=2, hemp=0)
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
    print(f'{usage}%')
