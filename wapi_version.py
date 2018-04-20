# just a stupid script to tell me what the WAPI version is for INFOBLOX

import requests
import json
import re

url = 'https://192.168.254.50/wapidoc'
r = requests.get(url, auth=('admin', 'infoblox'), verify=False)
if r.status_code == requests.codes.ok:
    lines = r.text.split('\n')
    for line in lines:
        reg = re.compile(r'Infoblox WAPI ([0-9\.]+)[^0-9]')
        tmp = re.search(reg, line, flags=0)
        if tmp:
            wapi_version = tmp.group(1)

print ('WAPI version is {}'.format(wapi_version))
