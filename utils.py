# pip install git+https://github.com/zphang/transformers@llama_push

import numpy as np 
import requests 
from tqdm.auto import tqdm

from settings import * 

def kakao_map(address):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
    api_key = '0763f0b11a74de2c93c8cca992482a38'
    header = {'Authorization': 'KakaoAK ' + api_key}
    results = requests.get(url, headers=header).json()['documents']
    if results == []:
        return None
    else:  
        results = results[0]['address']
        return float(results['x']), float(results['y'])
    
    
def getLongLat(addr):
    Long, Lat = [], []
    for i in tqdm(range(len(addr)), total=len(addr)):
        location = kakao_map(addr[i])
        if location:
            long, lat = location
            Long.append(long)
            Lat.append(lat)
        else:
            Long.append(np.NaN)
            Lat.append(np.NaN)
    return Long, Lat


def LabelEncoder(value, types=types):

    type_dict = dict({t:i for i, t in enumerate(types)})
    
    return type_dict[value]