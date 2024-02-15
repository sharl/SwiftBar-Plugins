#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# METADATA
# <xbar.title>Yeelight</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Sharl Morlaroll</xbar.author>
# <xbar.author.github>sharl</xbar.author.github>
# <xbar.desc></xbar.desc>
# <xbar.dependencies>python3.11+, yeelight</xbar.dependencies>
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>true</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>true</swiftbar.hideSwiftBar>

import os
import sys

from yeelight import Bulb, discover_bulbs

bulbs = discover_bulbs()

if len(sys.argv) == 1:
    icon = '| templateImage=iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAA8FBMVEXzJjXzJjTzJTTzJzbyJjXyJDPyIC/zKDfzLTvyPkvxFyfyGSnzKTjyPUvyHy7yQlD88vP6vsL0XWjxHy7yFyfxHi788/P0RFHyHi7yQk/9+fn76On+///85+j2fof2fob9///++vr0Q1DyQE3ySVXzOkf4r7T++/v++/z5sLXzPEnzRlP0QU/3lZzyITDwCBn7ycz7zdDwCRr3kpnzQU7zJDPyKzn4qK7////6vMDxDx/7ztH70tbxDyD5ub34pqzyKzrzRFD1ZnHxFCT7zND70NTxFSX1Y23yFybyJTTzKTfyGyvyIzLzRVLyIzPzKDZ4s6/dAAAAAWJLR0Q4oAel1gAAAAd0SU1FB+cLFQ8sB3uLrhYAAACzSURBVBjTfY7HEoJAEAXH3YVV0VUQMyrmnMWcM2L4/79xUasMB1/NpfsyDQAO+JoDwc8QYPKQiGAO/ASRUoIQoVQUOBLB6XJL4PGA5PY6BQDMfH5ZCahqUJFD4QjmIhqLa4lkKqHH0xlmi6yeyxeKpXKlqtVeot5ottodsav1uACjPxiOxpPpbK4tlob91lBX6812tz/0jgaYds+JWedL9Wqx07MQTEyBReCGzXe/iT/p/+7zzhGW4oMj8wAAAF9lWElmSUkqAAgAAAABAGmHBAABAAAAGgAAAAAAAAABAIaSBwAyAAAALAAAAAAAAABBU0NJSQAAADEuNzIuMS0yM0otSUpBNzJSTk1UT01HQzZFSllSTzVGTExCSFkuMC4yLTdtdyNtAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIzLTExLTIxVDA2OjQ1OjIyKzA5OjAwo5JPPwAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMy0xMS0yMVQwNjo0NDowNyswOTowMC0QtGcAAAAASUVORK5CYII='

    print(icon)
    print('---')

    for bulb in bulbs:
        ip = bulb['ip']
        cap = bulb['capabilities']
        print(f"{ip} {cap['model']} | terminal=false bash='{sys.argv[0]}' param1={ip}")
else:
    ip = sys.argv[1]
    bulb = Bulb(ip)
    bulb.toggle()
