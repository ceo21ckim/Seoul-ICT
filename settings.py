import os 

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data')
IMG_DIR = os.path.join(BASE_DIR, 'image')

if not os.path.exists(IMG_DIR):
    os.mkdir(os.path.join(BASE_DIR, 'image'))
    
    
types = ['백화점', '교통시설', '시장', '대형마트', '전시시설', '자연경관(하천/해양)', '테마공원', '쇼핑몰',
    '호텔', '도시공원', '자연공원', '복합관광시설', '레저스포츠시설', '기타관광', '종교성지', '공연시설',
    '육상레저스포츠', '기타문화관광지']

color_list = ['beige', 'darkgreen', 'darkpurple', 'orange', 'blue', 
              'lightblue', 'darkblue', 'darkred', 'lightred', 'green', 
              'lightgray', 'white', 'pink', 'cadetblue', 'purple', 
              'gray', 'red', 'black', 'lightgreen']
color_dict = dict({i:value for i, value in enumerate(color_list)})