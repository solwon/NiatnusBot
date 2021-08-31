import json
import datetime
import re

import helper

from bs4 import BeautifulSoup

secrets = json.loads(open('secrets.json').read())
weapon_start = datetime.datetime(2013, 9, 14)
armor_start = datetime.datetime(2014, 3, 29, 12)


def lotto():
    now = datetime.datetime.now()

    # lotto weapon
    content = helper.safe_content(secrets['URL']['lt'], cookies=secrets['COOKIE'])
    if not content:
        return
    soup = BeautifulSoup(content, 'html.parser')
    weapon_name_today = soup.select_one('#lottery_eqname').string
    tickets_str = soup.select_one('#rightpane>div:nth-child(5)').string
    weapon_ticket_num = tickets_str.split(' ')[4]
    weapon_expiry = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=1)
    weapon_remain_time = str(weapon_expiry - now).split('.')[0]

    # lotto armor
    content = helper.safe_content(secrets['URL']['la'], cookies=secrets['COOKIE'])
    if not content:
        return
    soup = BeautifulSoup(content, 'html.parser')
    armor_name_today = soup.select_one('#lottery_eqname').string
    tickets_str = soup.select_one('#rightpane>div:nth-child(5)').string
    armor_ticket_num = tickets_str.split(' ')[4]
    armor_expiry = datetime.datetime(now.year, now.month, now.day, 12) + datetime.timedelta(days=1)
    armor_remain_time = str(armor_expiry - now).split('.')[0]

    # lotto yesterday
    weapon_key = (now - weapon_start).days
    armor_key = (now - armor_start).days

    # lotto yesterday weapon
    content = helper.safe_content(f"{secrets['URL']['lt']}&lottery={weapon_key}", cookies=secrets['COOKIE'])
    soup = BeautifulSoup(content, 'html.parser')
    weapon_y_name = soup.select_one('#lottery_eqname').string
    weapon_y_winner = soup.find(attrs={'style': 'margin:1px auto 0; width:440px'}).string
    tickets_str = soup.select_one('#rightpane>div:nth-child(5)').string
    weapon_y_ticket_num = tickets_str.split(' ')[4]

    # lotto yesterday armor
    content = helper.safe_content(f"{secrets['URL']['la']}&lottery={armor_key}", cookies=secrets['COOKIE'])
    soup = BeautifulSoup(content, 'html.parser')
    armor_y_name = soup.select_one('#lottery_eqname').string
    armor_y_winner = soup.find(attrs={'style': 'margin:1px auto 0; width:440px'}).string
    tickets_str = soup.select_one('#rightpane>div:nth-child(5)').string
    armor_y_ticket_num = tickets_str.split(' ')[4]

    return {
        'w_t_name': weapon_name_today,
        'w_t_ticket': weapon_ticket_num,
        'w_t_remain': weapon_remain_time,
        'a_t_name': armor_name_today,
        'a_t_ticket': armor_ticket_num,
        'a_t_remain': armor_remain_time,
        'w_y_name': weapon_y_name,
        'w_y_ticket': weapon_y_ticket_num,
        'w_y_winner': weapon_y_winner,
        'a_y_name': armor_y_name,
        'a_y_ticket': armor_y_ticket_num,
        'a_y_winner': armor_y_winner
    }


def orderbook(curr):
    content = helper.safe_content(secrets['URL'][curr], cookies=secrets['COOKIE'])
    if not content:
        return
    soup = BeautifulSoup(content, 'html.parser')
    hath_tables = soup.find_all('div', attrs={'style': 'float:left; width:220px'})
    bids = hath_tables[0].find_all(attrs={'style': 'text-align:right'})
    asks = hath_tables[1].find_all(attrs={'style': 'text-align:right'})
    bid_list, ask_list = [], []
    temp = []
    for i in range(len(bids)):
        if i % 2 == 0:
            amount = int(re.sub('\D', '', bids[i].string))
            temp = [amount]
        else:
            price = int(re.sub('\D', '', bids[i].string))
            temp.insert(0, price)
            bid_list.append(temp)
    for i in range(len(asks)):
        if i % 2 == 0:
            amount = int(re.sub('\D', '', asks[i].string))
            temp = [amount]
        else:
            price = int(re.sub('\D', '', asks[i].string))
            temp.insert(0, price)
            ask_list.append(temp)

    # print(bid_list)
    # print(ask_list)

    stats = soup.find_all('div', attrs={'style': 'float:left; width:449px'})
    stats_8h = stats[0].select_one('div')
    stats_24h = stats[1].select_one('div')
    nums_8h = [int(x) for x in re.sub('\D+', ' ', re.sub(',', '', str(stats_8h))).strip().split(' ')]
    nums_24h = [int(x) for x in re.sub('\D+', ' ', re.sub(',', '', str(stats_24h))).strip().split(' ')]

    recent = soup.select_one('#historytable').select('tr')[1].find_all('td')[4].string
    recent = int(re.sub('\D', '', recent))
    return {
        'bid_list': bid_list,
        'ask_list': ask_list,
        '8h_stats': nums_8h,
        '24h_stats': nums_24h,
        'recent': recent
    }
