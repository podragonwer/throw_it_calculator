#!/usr/bin/env python
# coding: utf-8

# In[11]:


import math
import json

def get_address(address_list):

    print(" 동/읍/면을 검색하세요 예) 신길1동 -> 신길")
    inp_str = input(" >>>주소 검색:")
    match_address = None

    while (1):
        matching = [s for s in address_list if inp_str in s]

        print ("\n--------검색결과--------\n")
        for i in range(len(matching)):
            print (i, matching[i])
        if not len(matching):
            print ("\n         없을무         \n")
        print ("\n------------------------\n")

        print ("\n 주소 번호를 입력하세요.")
        print (" 찾으시는 주소가 없다면 재검색! 예) 신길1동 -> 신길\n")

        inp_str = input(" >>>주소 검색/번호 입력:")
        try:
            match_idx = int(inp_str)
            if match_idx <= len(matching):
                match_address = matching[match_idx]
                break
        except:
            continue

    return match_address

def get_coordinates(feature_list, address):
    for region in feature_list:
        if region["address"] == address:
            coor = region["coordinates"]
            return coor
    print ("에러: 그런 주소가 없다는뎁쇼?")
    return

def _main_ ():
    print ("┏━━━━━━━━━━━━━━━━━━━━┓")
    print ("┃                    ┃")
    print ("┃ 던져줘! calculator!┃")
    print ("┃                    ┃")
    print ("┗━━━━━━━━━━━━━━━━━━━━┛")

    # constants
    R = 6371009 + 50             # 고도 50미터
    g = 9.8                     # m/s^2
    T = 25                     # °C
    vsound = (331.5 + 0.61*T) # m/s^2

    with open('coor_info.json', 'r', encoding="utf-8") as json_file:
        json_data = json.load(json_file)
        address_data = json_data["feature"]

    address_list = [sth["address"] for sth in address_data]
    
    gogo = 1

    while not (gogo in ['0', 'n', 'no', 'N', 'NO', 'No', 'nO']):
        
        print ("\n\n▶ 어디에서 던집니까? ◀\n")
        address1 = get_address(address_list)
        lon1, lat1 = get_coordinates(address_data, address1)
        print ("\n▶ 어디로 던지나요? ◀\n")
        address2 = get_address(address_list)
        lon2, lat2 = get_coordinates(address_data, address2)
        if (address1==address2):
            print ("연직 위로 던지세요!")            
            gogo = input("\n\n ▶ 한 번 더?")
            continue
        angle = float(input("던질 각도(°): ")) * math.pi / 180

        print ("출발지:", format(lat1, ".6f"), format(lon1, ".6f"))
        print ("도착지:", format(lat2, ".6f"), format(lon2, ".6f"))

        lon1 *= (math.pi / 180)
        lat1 *= (math.pi / 180)
        lon2 *= (math.pi / 180)
        lat2 *= (math.pi / 180)

        x1 = R * math.cos(lat1) * (abs(lon1-lon2))
        x2 = R * math.cos(lat2) * (abs(lon1-lon2))
        y = R * (abs(lat1-lat2))
        dist = math.sqrt( x1**2 + y**2 - x2*y*abs(x2-x1)/y )

        cos = math.cos(angle)
        sin = math.sin(angle)

        v0 = math.sqrt( dist*g / (2*cos*sin) )
        maxh = (v0 * sin)**2 / g
        t = dist/(v0*cos) #초
        min = int(t/60)
        sec = int(t%60)

        print ("던져야 할 거리:", format(dist/1000, ".2f"), "km")
        print ("초기속도:", format(v0/1000, ".2f"), "km/s = 마하", format(v0/vsound, ".2f"))
        print ("최고높이:",  format(maxh, ".2f"), "m")
        print ("걸리는 시간:", min, "분", sec, "초")
        
        gogo = input("\n\n ▶ 한 번 더?")

    
_main_()

# In[ ]:

###############################
# 행정동 경계 geojson파일 수정 #
###############################

# 파일 출처: https://github.com/vuski/admdongkor

# import numpy as np
# from collections import OrderedDict
# import json

# coor_data = []

# with open('./HangJeongDong_ver20190908.geojson', encoding='UTF8') as json_file:
#     json_data = json.load(json_file)
    
#     for region in json_data["features"]:
#         name = region["properties"]['adm_nm']
# #         address = name.split()
        
#         sum = np.sum(region['geometry']['coordinates'][0][0],0)
#         avg = sum/len(region['geometry']['coordinates'][0][0])
        
#         loc_coor = OrderedDict()
# #         loc_coor["address"] = name
# #         loc_coor["do/si"] = address[0]
# #         loc_coor["si/gun/gu"] = address[1]
# #         loc_coor["dong"] = address[2]
#         loc_coor["coordinates"] = list(avg)

#         coor_data.append(loc_coor)


# dumpdata = OrderedDict()
# dumpdata["name"] = "coordinate information"
# dumpdata["feature"] = coor_data
    

# with open('coor_info.json', 'w', encoding="utf-8") as make_file:
#     json.dump(dumpdata, make_file, ensure_ascii=False, indent="\t")

# with open('coor_info.json', 'r', encoding="utf-8") as json_file:
#     json_data = json.load(json_file)
#     address_data = json_data["feature"]

# cities = set()
# for region in address_data:
#     cities.add(region["do/si"])

# sigungu = dict()
# for city in cities:
#     tempset = set()

#     for region in address_data:
#         if region["do/si"] == city:
#             tempset.add(region["si/gun/gu"])

#     sigungu[city] = tempset

# full_address = dict()

# for city in cities:
#     full_address[city] = dict()
#     for dosi in sigungu[city]:
#         tempset = set()

#         for region in address_data:
#             if region["si/gun/gu"] == dosi:
#                 tempset.add(region["dong"])

#         full_address[city][dosi] = list(tempset)
        
# json_data["hierarchy"] = full_address

# with open('coor_info.json', 'w', encoding="utf-8") as make_file:
#     json.dump(json_data, make_file, ensure_ascii=False, indent="\t")


# In[ ]:




