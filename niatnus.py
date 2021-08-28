import asyncio
import random
import discord
import json

from discord.ext import commands
app = commands.Bot(command_prefix='!', help_command=None)
secrets = json.loads(open('secrets.json').read())
foods = {
    '특식': ['불고기', '찜닭', '닭도리탕', '스테이크', '월남쌈', '수육', '아귀찜', '낚지볶음', '탕수육', '깐풍기', '족발'],
    '찌개': ['비지찌개', '고추장찌개', '오징어찌개', '순두부찌개', '청국장', '동태찌개', '된장찌개', '김치찌개', '부대찌개'],
    '밥': ['카레', '비빔밥', '오므라이스', '김치볶음밥', '제육덮밥', '연어덮밥', '치킨마요덮밥', '카츠동', '오징어덮밥', '초밥', '마파두부밥', '쌈밥'],
    '면': ['라멘', '파스타', '냉면', '잔치국수', '비빔국수', '칼국수', '우동', '콩국수', '짜장면', '짬뽕', '쌀국수'],
    '국': ['육개장', '닭개장', '떡국', '소고기무국', '시래깃국', '갈비탕', '추어탕', '삼계탕', '대구탕', '순대국밥', '콩나물국밥', '뼈해장국'],
    '간편식': ['샌드위치', '프렌치토스트', '떡볶이', '시리얼', '샐러드', '밥버거', '핫도그', '편의점도시락', '김밥', '유부초밥', '햄버거']
}


@app.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(app.user.name)
    print('connection was succesful')
    await app.change_presence(status=discord.Status.online, activity=discord.Game('!도움'))


@app.command()
async def 도움(ctx):
    command = discord.Embed(title='명령어', description='명령어 목록', color=0x62c1cc)
    command.add_field(name='!안뇽', value='헬로 펭귄 출력', inline=False)
    command.add_field(name='!안녕', value='바이 펭귄 출력', inline=False)
    command.add_field(name='!해명해', value='해명해콘 출력', inline=False)
    command.add_field(name='!노루', value='ex)!노루 ooo > ooo를 구글 이미지 검색 후 출력', inline=False)
    command.add_field(name='!삭 or !a', value='!노루 명령어의 마지막 사진을 삭제(개발중)', inline=False)
    await ctx.send(embed=command)


@app.command()
async def 뭐먹지(ctx, *cat):
    if len(cat) == 0:
        await ctx.send(embed=menu_helper())
    else:
        if cat[0] == '전부':
            menus = []
            for k, v in foods.items():
                menus += v
            result = menus[random.randrange(0, len(menus))]
            response = discord.Embed(title="메뉴 추천", description=f'오늘은 {result}를 먹어보는 게 어떨까요?')
            await ctx.send(embed=response)
        elif cat[0] in ['특식', '찌개', '밥', '면', '국', '간편식']:
            result = foods[cat[0]][random.randrange(0, len(foods[cat[0]]))]
            response = discord.Embed(title="메뉴 추천", description=f'오늘은 {result}를 먹어보는 게 어떨까요?')
            await ctx.send(embed=response)
        else:
            await ctx.send(embed=menu_helper())


def menu_helper():
    response = discord.Embed(title='뭐먹지 가이드', description='뭐먹지 <종류>로 음식 종류를 특정할 수 있습니다', color=0x008275)
    response.add_field(name='전부', value='전체 목록에서 하나를 고릅니다', inline=False)
    response.add_field(name='특식', value='특별한 날에 어울리는 특별한 메뉴입니다', inline=False)
    response.add_field(name='찌개', value='찌개류 전반에서 하나를 고릅니다', inline=False)
    response.add_field(name='밥', value='덮밥, 볶음밥, 초밥 등 밥이 주역인 메뉴입니다', inline=False)
    response.add_field(name='면', value='더 이상의 설명이 必要韓紙?', inline=False)
    response.add_field(name='국', value='마 딴거먹을 돈이면 국밥이 몇그릇이냐?', inline=False)
    response.add_field(name='간편식', value='패스트푸드나 분식 등 가볍고 빠르게 먹기 좋은 메뉴입니다', inline=False)
    return response

app.run(secrets['BOT']['token'])
