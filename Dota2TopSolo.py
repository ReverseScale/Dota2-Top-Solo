# coding=utf-8

import requests
import json

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
# 存储初步处理后的详情数据
all_match_details_treated = []

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

# 500次调取接口获取500场比赛详情
for i in range(0, 500):
    current_match_id = str(all_match_id[i])
    url = get_detail_url_head + "key=" + steam_key + "&" + "match_id=" + current_match_id
    match_manager = requests.get(url)
    response_dict = match_manager.json()
    result_dict = response_dict['result']
    all_match_details.append(result_dict)
    print len(all_match_details)

# 写入json文件
file_object = open('matches_details.json', 'w')
json.dump(all_match_details, file_object)
file_object.close()


# 定义存储初步处理数据的类
class MatchDetailData:

    def __init__(self):
        self.our_gmp = 0.0
        self.our_hero_damage = 0.0
        self.our_tower_damage = 0.0
        self.their_gpm = 0.0
        self.kda = 0.0
        self.last_hits = 0.0
        self.denies = 0.0
        self.gpm = 0.0
        self.xpm = 0.0
        self.hero_damage = 0.0
        self.tower_damage = 0.0
        self.time = 0.0

# 初步处理数据
for match_detail in all_match_details:
    current_data = MatchDetailData()
    current_data.time = float(match_detail['duration'])
    current_players = match_detail['players']
    position_flag = 0

    for i in range(0, 10):
        current_player = current_players[i]
        if current_player['account_id'] == player_id:
            position_flag = i
            break

    if position_flag < 5:
        for i in range(0, 5):
            current_player = current_players[i]
            current_data.our_gmp += float(current_player['gold_per_min'])
            current_data.our_hero_damage += float(current_player['hero_damage'])
            current_data.our_tower_damage += float(current_player['tower_damage'])
        for i in range(5, 10):
            current_player = current_players[i]
            current_data.their_gpm += float(current_player['gold_per_min'])
    else:
        for i in range(5, 10):
            current_player = current_players[i]
            current_data.our_gmp += float(current_player['gold_per_min'])
            current_data.our_hero_damage += float(current_player['hero_damage'])
            current_data.our_tower_damage += float(current_player['tower_damage'])
        for i in range(0, 5):
            current_player = current_players[i]
            current_data.their_gpm += float(current_player['gold_per_min'])

    main_player = current_players[position_flag]
    kills = float(main_player['kills'])
    assists = float(main_player['assists'])
    deaths = float(main_player['deaths'])
    if deaths == 0.0:
        deaths = 1.0
    current_data.kda = (kills + assists) / deaths
    current_data.last_hits = float(main_player['last_hits'])
    current_data.denies = float(main_player['denies'])
    current_data.gpm = float(main_player['gold_per_min'])
    current_data.xpm = float(main_player['xp_per_min'])
    current_data.hero_damage = float(main_player['hero_damage'])
    current_data.tower_damage = float(main_player['tower_damage'])
    all_match_details_treated.append(current_data)

# 对象转字典
all_match_details_treated_dict = []
for match_detail_treated in all_match_details_treated:
    match_detail_treated_dict = match_detail_treated.__dict__
    all_match_details_treated_dict.append(match_detail_treated_dict)

# 写入json文件
file_object = open('matches_details_treated.json', 'w')
json.dump(all_match_details_treated_dict, file_object)
file_object.close()



