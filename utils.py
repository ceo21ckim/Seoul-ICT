# pip install git+https://github.com/zphang/transformers@llama_push

import numpy as np
import pandas as pd  
import requests 
import folium

from sklearn.cluster import KMeans
from tqdm.auto import tqdm

from settings import * 

def kakao_map(address):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
    api_key = '### Your API Key'
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


def plot_map(dataframe, save=True, fname='daegu.html'):
    c_long, c_lat = dataframe.loc[:, 'long'].mean(), dataframe.loc[:, 'lat'].mean()
    
    m = folium.Map(location=[c_lat, c_long],
                   zoom_start=15)

    for lon, lat, name, category in dataframe.loc[:, ['long', 'lat', 'name', 'category']].values:
        if lon:
            folium.Marker(
                location=[lat, lon], 
                popup = f'<b>{name}</b>', 
                icon = folium.Icon(color=color_dict[category], icon='bookmark')
            ).add_to(m)
    
    if save:
        m.save(os.path.join(IMG_DIR, fname))
    return m 

def plot_cluster(dataframe, n_cluster=3, save=True, fname='daegu_cluster.html'):
    c_long, c_lat = dataframe.loc[:, 'long'].mean(), dataframe.loc[:, 'lat'].mean()
    m = folium.Map(location=[c_lat, c_long],
                   zoom_start=15)

    kmeans = KMeans(init = 'k-means++', n_clusters = n_cluster, n_init = 5)
    kmeans.fit(dataframe.loc[:, ['lat', 'long']].values)
    
    cluster_centers = kmeans.cluster_centers_
    dataframe.loc[:, 'label'] = kmeans.labels_
    
    for i, (lat, lon) in enumerate(cluster_centers):
        folium.Circle(
            location = [lat, lon],
            popup = f'<b>Center {i}</b>', # after click
            radius = 8000,
            color = color_list[i],
            fill = True,
            alpha = 0.5
        ).add_to(m)

    for lat, lon, labels, name in dataframe.loc[:, ['lat', 'long', 'label', 'name']].values:
        folium.Marker(
            location=[lat, lon], 
            popup = f'<b>{name}</b>', 
            icon = folium.Icon(color=color_list[labels], icon='bookmark')
        ).add_to(m)

    if save:
        m.save(os.path.join(IMG_DIR, fname))
    return m 


def get_dataframe(path):
    tour = pd.read_csv(path, encoding='cp949')

    tour.rename({'분류':'category', 
                 '관광지명': 'name', 
                 '주소': 'address', 
                 '순위': 'rank'}, axis=1, inplace=True)
    tour.loc[:, 'category'] = tour.loc[:, 'category'].apply(LabelEncoder)
    tour.loc[:, 'long'], tour.loc[:, 'lat'] = getLongLat(tour.loc[:, 'address'].values)
    
    tour.dropna(inplace=True)
    tour = tour.loc[:, ['name', 'category','long', 'lat']].copy()
    return tour


def get_distance(v):
    NotImplementedError