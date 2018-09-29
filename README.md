# Meet me half way!


#### How to run local server

* 먼저 django가 설치되어 있어야 한다.
* `cd backend`로 `backend` 폴더로 이동한다.
* `pipenv run python manage.py runserver`를 실행한다.


<hr>

## api
### Data get

서울 지하철 노선도에 필요한 호선은  
**1-9호선, 인천1호선, 분당선, 경의선, 신분당선, 공항철도, 중앙선, 경춘선, 수인선**이 있다.  
그중 먼저 1-8호선에 대해서 실험하고, 그 외의 선을 추가하는 방식을 하자.  


#### Desired data format

하나의 제이슨에 'stations'를 키로 하는 역 정보들과,  
'lines'라고 하는 호선 정보,  
부가적으로 강을 표시하시 위한 'river' 값을 필요로 함.  

<br>

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

<br>

#### Data source

* 대한민국 지하철 역사 정보 : https://www.data.go.kr/dataset/15013205/standard.do
* 서울 지하철 1-8호선 역 정보 : https://www.data.go.kr/dataset/15003842/fileData.do

#### Data preprocess


<br>

#### Data save as json


<br>


### Data parse


### half-way
