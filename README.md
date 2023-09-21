# Seoul-ICT

## Requirements

```
boto3 <=1.15.18
gluonnlp >= 0.6.0, <=0.10.0
tqdm
torch
transformers
pandas
numpy
folium
scikit-learn
accelerate
sentencepiece
mxnet
```

## Docker Settings

**1.clone this repository**
``` 
https://github.com/ceo21ckim/Seoul-ICT.git
cd Seoul-ICT
```

**2.build Dockerfile**
```
docker build --tag seoul_ict:1.0 .
```

**3.execute**

```
# Docker version 2.0 or later.
docker run -itd --runtime=nvidia --name ict -p 8888:8888 -v C:\Users\Name\:/workspace seoul_ict:1.0 /bin/bash
```

```
# Docker-ce 19.03 or later
docker run -itd --gpus all --name ict -p 8888:8888 -v C:\Users\Name\:/workspace seoul_ict:1.0 /bin/bash
```

도커의 버전이 `19.03`이거나 이후 버전인 경우에는 `NVIDIA`를 따로 설치하지 않고 `--gpus all`만 사용하더라도 GPU 사용이 가능합니다. `pytorch`의 경우 작업 환경을 `/workspace`로 설정하기 때문에 동일하게 `/workspace`로 지정해주었습니다. port 연결을 통해 localhost에서도 접속이 가능합니다. `https://localhost:8888`


**4.use jupyter notebook**
```
docker exec -it ict bash

jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root
```
`port`는 처음 실행할 때 연결한 `port`를 지정하시면 됩니다. 


## Example

```
### 질문: 동성로에 대해서 설명해줘

### 답변: 동성로는 대구광역시의 중앙에 위치한 지역으로, 동성로를 따라 대구의 대표적인 번화가들이 자리 잡았습니다.
          1958년에는 대구 비행장 활주로가 있던 곳에 근대적인 쇼핑센터인 '동아백화점'이 들어섰으며,
          이후 1960년대부터는 서문시장과 함께 발달하면서 영남지역의 경제적 중심지 역할을 했습니다.
```


### KAKAO API Sample
```

{'documents': [{'address': {'address_name': '서울 강남구 논현동 241-7',
    'b_code': '1168010800',
    'h_code': '1168053100',
    'main_address_no': '241',
    'mountain_yn': 'N',
    'region_1depth_name': '서울',
    'region_2depth_name': '강남구',
    'region_3depth_h_name': '논현2동',
    'region_3depth_name': '논현동',
    'sub_address_no': '7',
    'x': '127.041258693516',
    'y': '37.5166119773031'},
   'address_name': '서울 강남구 선릉로 669',
   'address_type': 'ROAD_ADDR',
   'road_address': {'address_name': '서울 강남구 선릉로 669',
    'building_name': '상경빌딩',
    'main_building_no': '669',
    'region_1depth_name': '서울',
    'region_2depth_name': '강남구',
    'region_3depth_name': '논현동',
    'road_name': '선릉로',
    'sub_building_no': '',
    'underground_yn': 'N',
    'x': '127.041258693516',
    'y': '37.5166119773031',
    'zone_no': '06099'},
   'x': '127.041258693516',
   'y': '37.5166119773031'}],
 'meta': {'is_end': True, 'pageable_count': 1, 'total_count': 1}} 

```
