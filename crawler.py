import json
import datetime

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


def hath():
    content = helper.safe_content(secrets['URL']['hath'], cookies=secrets['COOKIE'])
    if not content:
        return
    soup = BeautifulSoup(content, 'html.parser')
    hath_tables = soup.find_all('div', attrs={'style': 'float:left; width:220px'})
