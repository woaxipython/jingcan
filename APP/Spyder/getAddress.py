import json

import requests


def getAddress():
    url = "https://restapi.amap.com/v3/config/district?keywords=中国&subdistrict=3&key=5197e1e4f1b4a12ed28c8e45bf7cb5c8"
    response = requests.get(url=url)
    City = response.json()['districts']
    for districts in City[0]['districts']:
        for district in districts["districts"]:
            for distric in district['districts']:
                yield (districts['name'], district['name'],distric['name'])


if __name__ == '__main__':
    results = getAddress()
    for result in results:
        print(result)
