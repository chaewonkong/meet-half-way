"""Generate data from line No.1 to line No.8 formatted dedicated to d3-tube-map


When you execute this file, this script gets subway API from
'http://data.seoul.go.kr/dataList/datasetView.do?infId=OA-12761&infSeq=1&srvType=A#'
and preprocess it into one json file.

File format fits d3-tube-map data format.

The result json file can be found '/data/results/data.json'
"""

import json
import requests
import time


data = {
        'stations': [],
        'lines': [],
       }


# 1. stations 삽입.

key = '727369756c73686f3131347266787375'
lines = [n for n in range(1, 8+1)]
# 1 ~ 8호선 색상
colors = ['#0052A4', '#009D3E', '#EF7C1C', '#00A5DE', '#996CAC', '#CD7C2F', '#747F00', '#EA545D']
URL_PREFIX = 'http://swopenAPI.seoul.go.kr/api/subway/' + key + '/json/stationByLine/1/100/'
go = True


for n in lines:
    url = URL_PREFIX + str(n) + '호선'
    results = requests.get(url)
    if results.status_code != 200:
        print(results.status_code, + ', ' + str(n) + "호선 데이터 GET 중 열린 데이터 광장의 API 서버 오작동. 다음에 다시 시도해주세요.")
        go = False
        break
    stations = results.text
    stations = json.loads(stations)
    print(n, stations.keys())

    # 1 ~ 8 호선을 lines에 추가

    data['lines'].append({
        "number": n,
        "name": str(n) + '호선',
        "label": str(n) + '호선',
        "color": colors[n-1],
        "shiftCoords": [0, 0],
        "distanceFromPrevious": 120,
        "nodes": [],
    })

    # 1 ~ 8 호선별로 역마다 순회하며, `stations`와 `lines`의 `nodes`추가
    if 'lineList' in stations:
        for each_st in stations['lineList']:
            data['stations'].append({
                'name': str(each_st['statnNm']),
                'label': str(each_st['statnNm']),
                'place_id': str(each_st['statnId']),
                'position': {
                    'lat': 0,
                    'lon': 0,
                }
            })
            data['lines'][-1]['nodes'].append({
              "coords": [0, 0],
              "name": str(each_st['statnNm']),
              "labelPos": "S"
            })
    else:
        break

    time.sleep(5)



# 2. 호선 삽입



# 3. json dump
if go:
    with open('../results/data.json', 'w') as fp:
        fp.write(str(data))
