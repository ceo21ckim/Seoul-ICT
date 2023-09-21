import os 
import glob 
import pandas as pd 

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data')
IMG_DIR = os.path.join(BASE_DIR, 'image')

if not os.path.exists(IMG_DIR):
    os.mkdir(os.path.join(BASE_DIR, 'image'))

def get_unique_type():
    types = []
    for fname in glob.glob(os.path.join(DATA_DIR, '*')):
        u_type = pd.read_csv(fname, encoding='cp949').loc[:, '분류'].unique().tolist()
        types.extend(u_type)
    return list(set(types))

    
TYPE = get_unique_type()

color_list = ['orange', 'blue', 'green', 'beige', 'darkgreen', 'darkpurple', 
              'lightblue', 'darkblue', 'darkred', 'lightred', 'lightgray', 
              'white', 'pink', 'cadetblue', 'purple', 'gray', 'red', 'black', 'lightgreen'] * 2

color_dict = dict({i:value for i, value in enumerate(color_list)})