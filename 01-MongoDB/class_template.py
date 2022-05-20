# -*- coding: utf-8 -*-
# @Author: AI悦创
# @Date:   2022-05-13 07:49:15
# @Last Modified by:   aiyc
# @Last Modified time: 2022-05-13 11:35:18
import requests

url = "http://photogz.photo.store.qq.com/psc?/V10Wm75u1kBQ22/8v1c6OdZLSE3kzDE6fnRyglSUZD.KyVUe96.CzIj4npmvBZ4WMXsXd7DbnfP5m26KxaZgzIcsADVb6*1m.duOHeMSjVNmxeN7lyrvuTjg2I!/m&bo=QAUABAAAAAAAAGc!&rf=viewer_311"

html = requests.get(url).content
with open("image.png", mode="wb") as f:
    f.write(html)