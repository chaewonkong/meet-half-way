# Meet me half way!


#### How to run local server

* 먼저 django가 설치되어 있어야 한다.
* `cd backend`로 `backend` 폴더로 이동한다.
* `pipenv run python manage.py runserver`를 실행한다.


<hr>

## Data
### Data get

서울 지하철 노선도에 필요한 호선은  
**1-9호선, 인천1호선, 분당선, 경의선, 신분당선, 공항철도, 중앙선, 경춘선, 수인선**이 있다.  
그중 먼저 1-8호선에 대해서 실험하고, 그 외의 선을 추가하는 방식을 하자.  


#### Desired data format

우리는 먼저 [d3-tube-map](https://bl.ocks.org/johnwalley/9b6d8af7a209b95c5b9dff99073db420)이라는 D3 확장 라이브러리를 사용해 구현하려고 한다.  
이 라이브러리는 사용자에게 입력 데이터 형식을 지정해주었는데 그것은 아래와 같다.


```json

{
  "stations": {
    "AlexandraArms": {
      "name": "Alexandra Arms",
      "label": "Alexandra\nArms",
      "place_id": "ChIJaVrou4hw2EcROetQMMOP12M",
      "address": "22 Gwydir St, Cambridge CB1 2LL",
      "website": "http://www.thealexcambridge.com/",
      "phone": "01223 324441",
      "position": {
        "lat": 52.20386,
        "lon": 0.139356
      }
    },
    "Alma": {
      "name": "Alma",
      "label": "Alma",
      "place_id": "ChIJF5v8q55w2EcRWbfRNUQNPmE",
      "address": "26 Russel Court, Cambridge, CB2 1HW",
      "website": "http://www.thealmacambridge.co.uk/",
      "phone": "01223 316722",
      "position": {
        "lat": 52.195982,
        "lon": 0.125493
      }
    },
    ...,
  "lines": [
    {
      "name": "Town",
      "label": "Town",
      "color": "#FFD600",
      "shiftCoords": [0, 0],
      "distanceFromPrevious": 120,
      "nodes": [
        {
          "coords": [14, -4],
          "name": "Mill",
          "labelPos": "S"
        },
    },
  ]
    ...,
  "river": {
    "name": "River",
    "label": "River",
    "shiftCoords": [0, 0],
    "nodes": [
      {
        "coords": [-14, -28]
      },
      {
        "coords": [5, -8]
      },
      {
        "coords": [6, -6]
      },
      {
        "coords": [6, 12]
      },
      {
        "coords": [7, 14]
      },
      {
        "coords": [9, 16]
      },
      {
        "coords": [11, 17]
      },
      {
        "coords": [50, 17]
      },
      {
        "coords": [52, 18]
      },
      {
        "coords": [76, 42]
      }
    ]
  }
```

하나의 json 파일에  

1. `stations`를 키로 하는 역 정보들과,  
2. `lines`라고 하는 호선 정보,  
3. 부가적으로 강 등을 표시하시 위한 커스텀 정보를 필요로 함.  

<br>

`stations`는 호선 정보 없는 역들의 모음으로 개별 역은 다음과 같다.  

```json
    "AlexandraArms": {
      "name": "Alexandra Arms",
      "label": "Alexandra\nArms",
      "place_id": "ChIJaVrou4hw2EcROetQMMOP12M",
      "position": {
        "lat": 52.20386,
        "lon": 0.139356
      }
```

이 중 우리 앱에 필요한 정보만 남기면 다음과 같다.

<br>


`lines`는 `1호선`, `2호선` 등 각 호선에 대한 정보가 담긴다.  
개별 호선의 정보 양식은 다음과 같다.  

```json
    {
      "name": "5호선",
      "label": "5호선",
      "color": "violet",
      "shiftCoords": [0, 0],
      "distanceFromPrevious": 120",
      "nodes": [
        {
          "coords": [14, -4],
          "name": "Mill",
          "labelPos": "S"
        },
    },
```

여기서 `shiftCoords`, `distanceFromPrevious`는 당장은 잘 모르겠고...  
`nodes`는 호선의 각 역을 순서대로 집어넣은 정보들로, **`name` 속성이 `stations`의 한 역과 이름이 매칭되어야 한다.**  
 

<br>

#### Data source

* 대한민국 지하철 역사 정보 : https://www.data.go.kr/dataset/15013205/standard.do
* 서울 지하철 1-8호선 역 정보, 환승 시 시간정보 : https://www.data.go.kr/dataset/15003842/fileData.do

##### API

**API 정보들은 인증키의 유효기간이 3개월이다.** 이후에 갱신해야 하는 듯
* 서울시 역외부코드로 지하철역 위치 조회 ★★★★★ : http://data.seoul.go.kr/dataList/datasetView.do?infId=OA-117&srvType=A&serviceKind=1&currentPageNo=1
* 서울시 지하철 호선별 역사경유 정보 : http://data.seoul.go.kr/dataList/datasetView.do?infId=OA-12761&infSeq=1&srvType=A#

<br>

#### Data preprocess

앞서 언급한 1~3번 중 1, 2번이 지하철 노선도를 그리기 위한 핵심 데이터이기 때문에 이 둘을 우선적으로 데이터화한다.  
서울에는 주요 1 ~ 8호선 이외에 중앙선 등 잡다한 호선이 많은데 일단 **1호선부터 8호선까지만 구현하고 다른 호선을 추가하는 방식을 쓰자**  

<br>

##### 1. 역들의 정보를 `stations`로 저장하기

역들의 정보는 호선 정보 없이 모두 하나에 저장할 수 있다. 그 키값을 'stations'로 할 것.


```python


```


##### 2. 호선 정보를 `lines`로 저장하기



<br>

#### Data save as json & results


<br>


### Data parse


<hr>
<br>
<br>

## Api
### half-way
