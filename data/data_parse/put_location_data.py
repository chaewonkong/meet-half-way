"""Put locations of each station into data.json


The file to parse is '서울시 역코드로 지하철역 위치 조회.csv' and it's from
'http://data.seoul.go.kr/dataList/datasetView.do?infId=OA-118&srvType=S&serviceKind=1'

알고리즘 분석

1. data load:
    data.json을 dict로 반직렬화하고 data 변수에 저장한다.
2. '서울시...' 파일을 csv 모듈로 로드 후 한 줄씩 읽으며, 'X좌표(WGS)', 'Y좌표(WGS)' 부분을 data의 위경도에 추가한다. 이때 업데이트 할 목록은 한 역당,
    - stations[i][pos][lat]과 stations[i][pos][long],
    - lines[i][nodes][coords] = [x, y]
3. data를 data.json으로 다시 직렬화한다.
"""
import csv


# 1.
with open('../source/서울시 역코드로 지하철역 위치 조회.csv', newline='') as fp:
    reader = csv.reader(fp)
    column, *location_data = list(reader)
    n_index = column.index('전철역명')
    x_index, y_index = column.index('X좌표(WGS)'), column.index('Y좌표(WGS)')
    print(len(location_data))


# 2.
with open('../results/data.json') as fp:
    data = eval(fp.read())
    print(len(data))

# 2.1
for stn in location_data:
    if stn[n_index] and stn[x_index] and stn[y_index]:
        name, lat, lon = stn[n_index], float(stn[x_index]), float(stn[y_index])

    # data['stations']
    for stn in data['stations']:
        if name in stn['name']:
            stn['position']['lat'] = lat
            stn['position']['lon'] = lon

    # data['lines']
    for line in data['lines']:
        for node in line['nodes']:
            if name in node['name']:
                node['coords'] = [lat, lon]


# json은 큰따옴표만 써야 한다.
with open('new-data.json', 'w') as fp:
    fp.write(str(data).replace("'", '"'))

