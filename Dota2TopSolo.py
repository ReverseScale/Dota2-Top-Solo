# coding=utf-8

import requests

# steam密钥
steam_key = "46B889517E8A36598BCE2C18F38A0E3F"
# 选手steam账户ID
player_id = "106863163"
# 比赛开始id
match_start_id = ""
# get matches url head
get_match_url_head = "https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?"
# get match detail head
get_detail_url_head = "https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?"
# 存储所有比赛id的list
all_match_id = []
# 存储所有比赛详情list
all_match_details = []
# 5次遍历取到500场比赛id(每次获取上限为100场)
for i in range(0, 5):
    # 拼接后的url
    url = get_match_url_head + "key=" + steam_key + "&" + "account_id=" + player_id + "&" + "start_at_match_id=" + match_start_id
    match_manager = requests.get(url)
    response_dict = match_manager.json()
    result_dict = response_dict['result']
    match_arr = result_dict['matches']

    for match in match_arr:
        match_id = match['match_id']
        all_match_id.append(match_id)
    last_id = all_match_id[-1]
    match_start_id = str(last_id)
    print (match_start_id)

print len(all_match_id)

# 500次调取接口获取500场比赛详情
for i in range(0, 500):
    current_match_id = str(all_match_id[i])
    url = get_detail_url_head + "key=" + steam_key + "&" + "match_id=" + current_match_id
    match_manager = requests.get(url)
    response_dict = match_manager.json()
    result_dict = response_dict['result']
    all_match_details.append(response_dict)
    print len(all_match_details)


# print (url)
# print type(url)
# print (response_dict)
# print type(response_dict)
# print (result_dict)
# print type(result_dict)
# print (match_arr)
# print type(match_arr)