import requests
import json
import random 
import networkx as nx
from typing import List
from googleplaces import GooglePlaces, types, lang, GooglePlacesError, ranking

# Insert your API key
API_KEY = "AIzaSyDKGfZlHdOhx1VxePjxsBYJqwnP5fFt2mo"

def get_lat_long(address:str):
    url ='https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, API_KEY)

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

def nearby_search_api():
    google_places = GooglePlaces(API_KEY)
    # You may prefer to use the text_search API, instead.
    query_result = google_places.nearby_search(language=lang.VIETNAMESE,
            lat_lng={'lat': 10.771892, 'lng': 106.657919}, keyword=None , 
            radius=50000, types=[types.TYPE_RESTAURANT] or [types.TYPE_CAFE])
    # If types param contains only 1 item the request to Google Places API
    # will be send as type param to fullfil:
    # http://googlegeodevelopers.blogspot.com.au/2016/02/changes-and-quality-improvements-in_16.html

    for place in query_result.places:
        # Returned places from a query are place summaries.
        print(place.name)
        print(place.geo_location)
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

if __name__ == '__main__':
    points = ["268 Lý Thường Kiệt, Phường 14, Quận 10, Thành phố Hồ Chí Minh",
          "Cầu vượt Ba tháng Hai, Phường 10 (Quận 10), Quận 10, Thành phố Hồ Chí Minh, Việt Nam",
          "Trung Tâm Vàng Bạc Đá Quý DOJI, Đường 3 Tháng 2, Phường 10 (Quận 10), Quận 10, Thành phố Hồ Chí Minh, Việt Nam",
          "819 Đ. 3 Tháng 2, Phường 7, Quận 10, Thành phố Hồ Chí Minh 008422, Việt Nam",
          "Bệnh Viện Trưng Vương Lý Thường Kiệt, phường 14, Quận 10, Thành phố Hồ Chí Minh, Việt Nam",
          "QMH4+8G Tân Bình, Thành phố Hồ Chí Minh, Việt Nam",
          "8 Đ. Thành Thái, Phường 14, Quận 10, Thành phố Hồ Chí Minh 70000, Việt Nam",
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
          "Big C Miền Đông, 268 Tô Hiến Thành, Phường 15, Quận 10, Thành phố Hồ Chí Minh 700000, Việt Nam"
          "247/73 Bà Hạt, Phường 4, Quận 10, Thành phố Hồ Chí Minh, Việt Nam",
          "469 Đ. Nguyễn Hữu Thọ, Tân Hưng, Quận 7, Thành phố Hồ Chí Minh, Việt Nam",
          "1365/1, An Phú Đông, Quận 12, Thành phố Hồ Chí Minh, Việt Nam",
          "46 Bạch Đằng, Phường 2, Tân Bình, Thành phố Hồ Chí Minh 736464, Việt Nam",
          "Trường Sơn, Phường 2, Tân Bình, Thành phố Hồ Chí Minh, Việt Nam",
          "261 Đ. Sư Vạn Hạnh, Phường 9, Quận 10, Thành phố Hồ Chí Minh 700000, Việt Nam",
          "341 Đ. Sư Vạn Hạnh, Phường 10, Quận 10, Thành phố Hồ Chí Minh, Việt Nam",
          "292 Đ. Đinh Bộ Lĩnh, Phường 26, Bình Thạnh, Thành phố Hồ Chí Minh 70000, Việt Nam",
          "RM7G+79 Gò Vấp, Thành phố Hồ Chí Minh, Việt Nam",
          "75 Đường Số 18, Phường 8, Gò Vấp, Thành phố Hồ Chí Minh, Việt Nam",
          "78 Đ. Hồ Thị Kỷ, Phường 1, Quận 10, Thành phố Hồ Chí Minh, Việt Nam",
          "42/42E Tôn Thất Thiệp, Bến Nghé, Quận 1, Thành phố Hồ Chí Minh, Việt Nam",
          "533 Bà Hạt, Phường 8, Quận 10, Thành phố Hồ Chí Minh, Việt Nam",
          "87 Đ. Trần Khắc Chân, Phường Tân Định, Quận 1, Thành phố Hồ Chí Minh 70000, Việt Nam",
          "22 Đường Nguyễn An Ninh, Phường 14, Bình Thạnh, Thành phố Hồ Chí Minh 70000, Việt Nam",
          "577 Đ. Sư Vạn Hạnh, Phường 12, Quận 10, Thành phố Hồ Chí Minh, Việt Nam",
          "402 Đ. Trần Phú, Phường 7, Quận 5, Thành phố Hồ Chí Minh, Việt Nam",
          "84 Đ. Đặng Văn Ngữ, Phường 10, Phú Nhuận, Thành phố Hồ Chí Minh, Việt Nam",
          "30 Đ. Nguyễn Thị Minh Khai, Bến Nghé, Quận 1, Thành phố Hồ Chí Minh, Việt Nam",
          "18 Đ. Ký Hoà, Phường 11, Quận 5, Thành phố Hồ Chí Minh, Việt Nam",
          "36 Đ. Hồ Tùng Mậu, Bến Nghé, Quận 1, Thành phố Hồ Chí Minh, Việt Nam",
          "2 Đ. số 9, Khu đô thị Him Lam, Quận 7, Thành phố Hồ Chí Minh, Việt Nam",
          "68 Đ3, Trường Thạnh, Quận 9, Thành phố Hồ Chí Minh, Việt Nam",
          "Toà nhà The CBD Premium Home, 125 Đồng Văn Cống, Phường Thạnh Mỹ Lợi, Thủ Đức, Thành phố Hồ Chí Minh 700000, Việt Nam",
          "2 Nguyễn Bỉnh Khiêm, Bến Nghé, Quận 1, Thành phố Hồ Chí Minh 700000, Việt Nam",
          "28 Võ Văn Tần, Phường 6, Quận 3, Thành phố Hồ Chí Minh, Việt Nam",
          "2 Nguyễn Bỉnh Khiêm, Bến Nghé, Quận 1, Thành phố Hồ Chí Minh, Việt Nam",
          "65 Lý Tự Trọng, Bến Nghé, Quận 1, Thành phố Hồ Chí Minh, Việt Nam",
          "QMGW+Q4 Quận 1, Thành phố Hồ Chí Minh, Việt Nam",
          "120 Xa Lộ Hà Nội, Thành Phố, Thủ Đức, Thành phố Hồ Chí Minh, Việt Nam",
          "4FR6+JJ Củ Chi, Thành phố Hồ Chí Minh, Việt Nam",
          "01 Công xã Paris, Bến Nghé, Quận 1, Thành phố Hồ Chí Minh 70000, Việt Nam",
          "52 Đ. Mạc Đĩnh Chi, Đa Kao, Quận 1, Thành phố Hồ Chí Minh, Việt Nam",
          "91 Hai Bà Trưng, Bến Nghé, Quận 1, Thành phố Hồ Chí Minh, Việt Nam",
          "215 Lý Tự Trọng, Phường Bến Thành, Quận 1, Thành phố Hồ Chí Minh, Việt Nam",
          "85 Đ. Nguyễn Cư Trinh, Phường Nguyễn Cư Trinh, Quận 1, Thành phố Hồ Chí Minh 000000, Việt Nam",
          "102/26 Đ. Cống Quỳnh, Phường Phạm Ngũ Lão, Quận 1, Thành phố Hồ Chí Minh 700000, Việt Nam",
          "168 Đ. Võ Văn Kiệt, Phường Cầu Ông Lãnh, Quận 1, Thành phố Hồ Chí Minh 70000, Việt Nam",
          "39 Đ. Bùi Thị Xuân, Phường Phạm Ngũ Lão, Quận 1, Thành phố Hồ Chí Minh, Việt Nam",
          "14 Số 45, Phường 6, Quận 4, Thành phố Hồ Chí Minh, Việt Nam",
          "89/19 Đoàn Văn Bơ, Phường 12, Quận 4, Thành phố Hồ Chí Minh, Việt Nam",
          "30 Nguyễn Trường Tộ, Phường 12, Quận 4, Thành phố Hồ Chí Minh, Việt Nam",
          "144 Đ. Khánh Hội, Phường 6, Quận 4, Thành phố Hồ Chí Minh, Việt Nam",
          "75 Lê Quốc Hưng, Phường 12, Quận 4, Thành phố Hồ Chí Minh, Việt Nam",
          "14b Đ. 46, Phường 5, Quận 4, Thành phố Hồ Chí Minh 754000, Việt Nam",
          "88 Đ. Hoàng Diệu, Phường 12, Quận 4, Thành phố Hồ Chí Minh, Việt Nam",
          "243/29G Tôn Đản, Phường 15, Quận 4, Thành phố Hồ Chí Minh, Việt Nam",
          "24 Đường số 67, Tân Phong, Quận 7, Thành phố Hồ Chí Minh, Việt Nam",
          "482 Huỳnh Tấn Phát, Bình Thuận, Quận 7, Thành phố Hồ Chí Minh, Việt Nam",
          "865 Trần Xuân Soạn, Tân Hưng, Quận 7, Thành phố Hồ Chí Minh, Việt Nam",
          "494 Nguyễn Thị Thập, Tân Quy, Quận 7, Thành phố Hồ Chí Minh, Việt Nam",
          "C26 KDC Nam Long, E8 Đ. Phú Thuận, Phú Thuận, Quận 7, Thành phố Hồ Chí Minh, Việt Nam",
          "172 Đ. Lâm Văn Bền, Tân Quy, Quận 7, Thành phố Hồ Chí Minh, Việt Nam",
          "649 Trần Xuân Soạn, Tân Hưng, Quận 7, Thành phố Hồ Chí Minh, Việt Nam",
          "92 Số 17, Tân Quy, Quận 7, Thành phố Hồ Chí Minh, Việt Nam",
          "518 Nguyễn Thị Thập, Tân Quy, Quận 7, Thành phố Hồ Chí Minh, Việt Nam",
          "39 Lê Văn Lương, Tân Kiểng, Quận 7, Thành phố Hồ Chí Minh, Việt Nam",
          "205 Số 17, Tân Quy, Quận 7, Thành phố Hồ Chí Minh, Việt Nam",
          "387 Lê Văn Lương, Tân Hưng, Quận 7, Thành phố Hồ Chí Minh, Việt Nam",
          "107 Đ Tôn Dật Tiên, Tân Phú, Quận 7, Thành phố Hồ Chí Minh 72908, Việt Nam",
          "Hồ Bán Nguyệt/Phan Văn Chương/02 - 06 Phú Mỹ Hưng, Tân Phú, Quận 7, Thành phố Hồ Chí Minh 70000, Việt Nam",
          "143 Nguyễn Đức Cảnh, Tân Phong, Quận 7, Thành phố Hồ Chí Minh, Việt Nam",
          "101 Đ Tôn Dật Tiên, Tân Phú, Quận 7, Thành phố Hồ Chí Minh 07000, Việt Nam",
          "31-33 Khu Him Lam Khu Him Lam, Nguyễn Thị Thập, Tân Hưng, Quận 7, Thành phố Hồ Chí Minh, Việt Nam",
          "51-53 Nguyễn Thị Thập, Tân Hưng, Quận 7, Thành phố Hồ Chí Minh 700000, Việt Nam",
          "44-46 Đường Số 14, Khu đô thị Him Lam, Quận 7, Thành phố Hồ Chí Minh, Việt Nam",
          "502/55/5 Huỳnh Tấn Phát, Bình Thuận, Quận 7, Thành phố Hồ Chí Minh 70000, Việt Nam",
          "996 Huỳnh Tấn Phát, Tân Phú, Quận 7, Thành phố Hồ Chí Minh 700000, Việt Nam",
          "160 Đ. Phạm Hùng, Phường 5, Quận 8, Thành phố Hồ Chí Minh, Việt Nam",
          "389 Đ. Hưng Phú, Phường 9, Quận 8, Thành phố Hồ Chí Minh, Việt Nam",
          "174 D. Bá Trạc, Phường 2, Quận 8, Thành phố Hồ Chí Minh, Việt Nam",
          "395 Đ. Kinh Dương Vương, An Lạc, Bình Tân, Thành phố Hồ Chí Minh, Việt Nam",
          "217 Đ. Hồng Bàng, Phường 11, Quận 5, Thành phố Hồ Chí Minh, Việt Nam",
          "227 Đ. Nguyễn Văn Cừ, Phường 4, Quận 5, Thành phố Hồ Chí Minh, Việt Nam",
          "65A Đ. Lũy Bán Bích, Tân Thới Hoà, Tân Phú, Thành phố Hồ Chí Minh, Việt Nam",
          "128 Nguyễn Thị Nhỏ, Phường 15, Quận 11, Thành phố Hồ Chí Minh"]
    
    no_vertex = len(list(set(points)))
    print("Number of vertex: ", no_vertex)

    edges = []

    while len(edges) < 2*no_vertex:
        path = (random.randint(0,no_vertex), random.randint(0,no_vertex))
        if path not in edges:
            edges.append(path)

    print("Number of edges: ", len(edges))

    print({id:address for id, address in enumerate(points)})

    datapoints = dict()
    for id, address in enumerate(points):
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
    output["distances"] = distances
    with open("graph_map/data/graph.json", 'wb') as f:
        f.write(json.dumps(output,  ensure_ascii=False).encode("utf8"))

    exit(0)
    #########################################################################################################