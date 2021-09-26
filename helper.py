import requests
import datetime
import discord
import re

EMBED_COLOR = 0x62c1cc
BAN_WORDS = ['h@h', 'h&h', '변태집', 'hentai@home', 'e-hentai', 'exhentai']
BAN_EXCEPTIONS = ['forums.e-hentai.org']


def log(cat, message):
    now = datetime.datetime.now()
    with open('log.log', 'a+') as f:
        print(f'[{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}] {cat.upper()}: {message}')
        f.write(f'[{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}] {cat.upper()}: {message}\n')


def safe_content(url, cookies):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
    response = requests.get(url, cookies=cookies, headers=headers)
    if response.status_code == 200:
        log('info', 'Successfully got response')
        return response.content
    else:
        log('error', 'Connection could not be established')
        return False


def menu_helper():
    response = discord.Embed(title='뭐먹지 가이드', description='뭐먹지 <종류>로 음식 종류를 특정할 수 있습니다', color=0x62c1cc)
    response.add_field(name='전부', value='전체 목록에서 하나를 고릅니다', inline=False)
    response.add_field(name='특식', value='특별한 날에 어울리는 특별한 메뉴입니다', inline=False)
    response.add_field(name='찌개', value='찌개류 전반에서 하나를 고릅니다', inline=False)
    response.add_field(name='밥', value='덮밥, 볶음밥, 초밥 등 밥이 주역인 메뉴입니다', inline=False)
    response.add_field(name='면', value='더 이상의 설명이 必要韓紙?', inline=False)
    response.add_field(name='국', value='마 딴거먹을 돈이면 국밥이 몇그릇이냐?', inline=False)
    response.add_field(name='간편식', value='패스트푸드나 분식 등 가볍고 빠르게 먹기 좋은 메뉴입니다', inline=False)
    return response


def eulreul(kstr):
    m = re.search('[가-힣]+', kstr)
    if m:
        k = m.group()[-1]
        if (ord(k) - ord('가')) % 28 > 0:
            return '을'
        else:
            return '를'
    else:
        return ''


def youtube_validation(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return youtube_regex_match

    return youtube_regex_match


def is_mention(text):
    mention_str = r'<@!+\d*>'
    return re.match(mention_str, text)
