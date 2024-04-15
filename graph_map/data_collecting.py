import requests
import json
import networkx as nx
from typing import List

# Insert your API key
API_KEY = ""

def get_lat_long(address:str):
    url ='https://maps.googleapis.com/maps/api/geocode/json?key={1}&address={0}'.format(address, API_KEY)


    api_response = requests.get(url)
    api_response_dict = api_response.json()
    if api_response_dict['status'] == 'OK':
        latitude = api_response_dict['results'][0]['geometry']['location']['lat']
        longitude = api_response_dict['results'][0]['geometry']['location']['lng']
        return {'Latitude': latitude, 'Longitude': longitude}
    else:
        print(address)
        print("None location returned")
        return None
    
# distance in meter
def get_distance(source:str, dest:str):
    # Take source as input
    # url variable store url
    url ='https://maps.googleapis.com/maps/api/distancematrix/json?origins={}&destinations={}&key={}'.format(source, dest, API_KEY)
    # print(url)
    # Get method of requests modulet
    # return response object
    r = requests.get(url)
                        
    # json method of response object
    # return json format result
    x = r.json()

    # print the value of x
    # print(x)
    if x['status'] == 'OK':
        return x['rows'][0]['elements'][0]['distance']['value']
    else:
        print("None distance returned")
        return None

class DataPoint:
    def __init__(self, id:int, address:str, lat:float=None, long:float=None) -> None:
        self.__id = id
        self.__address = address
        self.__lat = lat  
        self.__long = long
    
    @property
    def id(self):
        return self.__id
    
    @property 
    def address(self):
        return self.__address
    
    @property
    def lat(self):
        return self.__lat
    
    @lat.setter
    def lat(self, lat:float):
        self.__lat = lat

    @property
    def long(self):
        return self.__long
    
    @long.setter
    def long(self, long:float):
        self.__long = long

class Distance:
    def __init__(self, source:DataPoint, dest:DataPoint, distance:int) -> None:
        self.__source = source
        self.__dest = dest
        self.__distance = distance

    @property
    def source(self):
        return self.__source
    
    @source.setter
    def source(self, source:DataPoint):
        self.__source = source

    @property
    def dest(self):
        return self.__dest
    
    @dest.setter
    def dest(self, dest:DataPoint):
        self.__dest = dest

    @property
    def distance(self):
        return self.__distance
    
    @distance.setter
    def distance(self, distance:int):
        self.__distance = distance

points = ["Trường Đại học Bách khoa - Đại học Quốc gia TP.HCM, Lý Thường Kiệt, phường 14, Quận 10, Thành phố Hồ Chí Minh",
          "Dinh Độc Lập, Phường Bến Thành, Quận 1, Thành phố Hồ Chí Minh, Việt Nam",
          "Cầu vượt Ba tháng Hai, Phường 10 (Quận 10), Quận 10, Thành phố Hồ Chí Minh, Việt Nam",
          "Trung Tâm Vàng Bạc Đá Quý DOJI, Đường 3 Tháng 2, Phường 10 (Quận 10), Quận 10, Thành phố Hồ Chí Minh",
          "819 Đ. 3 Tháng 2, Phường 7, Quận 10, Thành phố Hồ Chí Minh 008422, Việt Nam",
          "Bệnh Viện Trưng Vương Lý Thường Kiệt, phường 14, Quận 10, Thành phố Hồ Chí Minh, Việt Nam",
          "QMH4+8G Tân Bình, Thành phố Hồ Chí Minh, Việt Nam",
          "I ốt số, 8, Đ. Thành Thái, Phường 14, Quận 10, Thành phố Hồ Chí Minh, Việt Nam",
          "353 Tô Hiến Thành, Phường 14, Quận 10, Thành phố Hồ Chí Minh, Việt Nam",
          "531G Đ. Cách Mạng Tháng 8, Phường 13, Quận 10, Thành phố Hồ Chí Minh 72511, Việt Nam",
          "Công trường Dân Chủ, Võ Thị Sáu, Quận 3, Thành phố Hồ Chí Minh",
          "Tượng đài Công Nông Binh, QM9F+3QC, Phường 2, Quận 10, Thành phố Hồ Chí Minh, Việt Nam",
          "150 Đ. Lý Thái Tổ, Phường 2, Quận 3, Thành phố Hồ Chí Minh, Việt Nam",
          "241Bis Đ. Cách Mạng Tháng 8, Phường 4, Quận 3, Thành phố Hồ Chí Minh 700000, Việt Nam",
          "54B Đường Bà Huyện Thanh Quan, Võ Thị Sáu, Quận 3, Thành phố Hồ Chí Minh, Việt Nam",
          "125 Đ. Cách Mạng Tháng 8, Phường Phạm Ngũ Lão, Quận 1, Thành phố Hồ Chí Minh, Việt Nam",
          "85 Đ. Nguyễn Thị Minh Khai, Phường Bến Thành, Quận 1, Thành phố Hồ Chí Minh 71009, Việt Nam",
          "Squirrel Rights Agency, 159 Đ. Nam Kỳ Khởi Nghĩa, Võ Thị Sáu, Quận 3, Thành phố Hồ Chí Minh, Việt Nam",
          "130 Đ. Nguyễn Thị Minh Khai, Phường Bến Thành, 3, Thành phố Hồ Chí Minh, Việt Nam",
          "173/14 Đ. Nguyễn Thị Minh Khai, Phường 2, Quận 3, Thành phố Hồ Chí Minh, Việt Nam",
          "341 Đ. Sư Vạn Hạnh, Phường 10, Quận 10, Thành phố Hồ Chí Minh, Việt Nam",
          "55 Đ. Nguyễn Thị Minh Khai, Phường Bến Thành, Quận 1, Thành phố Hồ Chí Minh, Việt Nam",
          "Công viên Văn hóa Lê Thị Riêng, Đường Cách Mạng Tháng 8, Cư xá Bắc Hải, Phường 15, Quận 10, Thành phố Hồ Chí Minh",
          "Bệnh viện Nhân dân 115, 527 Đ. Sư Vạn Hạnh, Phường 12, Quận 10, Thành phố Hồ Chí Minh, Việt Nam",
          "183b Đ. Cách Mạng Tháng 8, Phường 5, Quận 3, Thành phố Hồ Chí Minh 700000, Việt Nam",
          "Big C Miền Đông, 268 Tô Hiến Thành, Phường 15, Quận 10, Thành phố Hồ Chí Minh 700000, Việt Nam"]

edges = [(0,6), (6,0),
         (0,5), (5,0),
         (4,5), (5,4),
         (6,7), (7,6),
         (4,2), (2,4),
         (5,8), (8,5),
         (7,8), (8,7),
         (8,2), (2,8),
         (7,22), (22,7),
         (8,25), (25,8),
         (25,9), (9,25),
         (8,25), (25,8),
         (25,23), (23,25),
         (23,20), (20,23),
         (2,20), (20,2),
         (20,3), (3,20),
         (9,10), (10,9),
         (3,10), (10,3),
         (2,11), (11,2),
         (11,3), (3,11),
         (10,13), (13,10),
         (11,13), (13,11),
         (11,12), (12,11),
         (13,24), (24,13),
         (12,24),(24,12),
         (12,19), (19,12),
         (19,15), (15,19),
         (24,15), (15,24),
         (13,17),
         (24,14),
         (17,21),
         (14,16),
         (15,16),
         (16,18),
         (18,21),
         (18,1)]

print({id:address for id, address in enumerate(points)})

datapoints = dict()
for id, address in enumerate(points):
    # if id == 21:
    point = DataPoint(id, address)
    loc = get_lat_long(address)
    if loc is not None:
        point.lat = loc["Latitude"]
        point.long = loc["Longitude"]
    datapoints[id] = point

distances = []
for edge in edges:
    source = datapoints[edge[0]].address
    dest = datapoints[edge[1]].address
    distances.append(get_distance(source, dest))


output = dict()
nodes = [datapoints[i].__dict__ for i in datapoints.keys()]
output["nodes"] = nodes
output["edges"] = edges
with open("graph.json", 'wb') as f:
    f.write(json.dumps(output,  ensure_ascii=False).encode("utf8"))