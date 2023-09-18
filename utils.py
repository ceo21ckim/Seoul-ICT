# pip install git+https://github.com/zphang/transformers@llama_push

import numpy as np
import pandas as pd  
import requests 
import folium

from branca.element import Figure
from sklearn.cluster import KMeans
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
    '''
    Input:
        addr: address
    Return:
        Long, Lat: Longitude and Latitude of address
    '''
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
    '''
    Input: 
        value: indicates string such as department store, shopping mall and tour spot.
    Return:
        num2label[value]: indicates numeric variable.
    '''
    label2num = dict({t:i for i, t in enumerate(types)})
    return label2num[value]

def LabelDecoder(value, types=types):
    # similar to LabelEncoder. Different from LabelEncdoer, it returns a label, not numeric a variable.
    num2label = dict({i:t for i, t in enumerate(types)})
    return num2label[value]
    

def plot_map(dataframe, save=False, fname='daegu.html'):
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


def plot_cluster(dataframe, n_cluster=3, save=False, fname='daegu_cluster.html'):
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


def plot_map_all(save=False, extension='html'):
    files = glob.glob(os.path.join(DATA_DIR, '*'))
    
    for file in files:
        fname = os.path.basename(file).split('.')[0]
        dataframe = get_dataframe(file)
        
        plot_map(dataframe, save=save, fname='.'.join([fname, extension]))
        plot_cluster(dataframe, save=save, fname='.'.join([fname +'_cluster', extension]))


def get_dataframe(path):
    '''
    Input:
        path: indicates file path.
    Return:
        tour: Return a data frame, which is preprocessed for efficient programming.
    '''
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


def get_route(src, dst):
    answer = []
    while dst:
        _min = float('inf')
        for i, v in enumerate(dst):
            dist = distance(src, v)
            if _min > dist:
                _min = dist 
                idx = i
        src = dst.pop(idx)
        answer.append(src)
    return answer


def plot_route(src, others, save=False, fname='route', extension='html'):
    fig = Figure(width=550,height=350)
    route = get_route(src, others)
    center = np.mean(route, axis=0).tolist()
    m = folium.Map(location=center, 
                zoom_start=10)
    fig.add_child(m)
    folium.PolyLine(locations = route,
                ).add_to(m)
    
    for lat, lon in route:
        folium.Marker(
            location=[lat,lon], 
            icon=folium.Icon('lightblue', icon='bookmark'), 
            
        ).add_to(m)
    
    if save:
        m.save(os.path.join(IMG_DIR, '.'.join([fname, extension])))
    return m 


def distance(src, dst, types='l2'):
    if types == 'l2':
        return np.sqrt(np.power(src[0]-dst[0], 2) + np.power(src[1]-dst[1], 2))
    
    elif types == 'l1':
        return np.abs(src[0]-dst[0]) + np.abs(src[1]-dst[1])