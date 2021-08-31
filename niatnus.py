import asyncio
import random
import discord
import json
import datetime

import crawler
import helper

from discord.ext import commands, tasks

app = commands.Bot(command_prefix='!', help_command=None)
secrets = json.loads(open('secrets.json').read())
# SQLite 연동해서 추가삭제 가능하도록 할 것
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
    print('connection was successful')
    await app.change_presence(status=discord.Status.online, activity=discord.Game('!도움'))


@app.command()
async def 도움(ctx):
    command = discord.Embed(title='니앗누스봇 매뉴얼', color=helper.EMBED_COLOR)
    command.add_field(name='!lotto, !로또', value='헬로 펭귄 출력', inline=False)
    command.add_field(name='!안녕', value='바이 펭귄 출력', inline=False)
    command.add_field(name='!해명해', value='해명해콘 출력', inline=False)
    command.add_field(name='!노루', value='ex)!노루 ooo > ooo를 구글 이미지 검색 후 출력', inline=False)
    command.add_field(name='!삭 or !a', value='!노루 명령어의 마지막 사진을 삭제(개발중)', inline=False)
    await ctx.send(embed=command)


@app.command()
async def 뭐먹지(ctx, *cat):
    if len(cat) == 0:
        await ctx.send(embed=helper.menu_helper())
    else:
        if cat[0] == '전부':
            menus = []
            for k, v in foods.items():
                menus += v
            result = menus[random.randrange(0, len(menus))]
            response = discord.Embed(title="메뉴 추천", description=f'오늘은 {result}를 먹어보는 게 어떨까요?, color=helper.EMBED_COLOR')
            await ctx.send(embed=response)
        elif cat[0] in ['특식', '찌개', '밥', '면', '국', '간편식']:
            result = foods[cat[0]][random.randrange(0, len(foods[cat[0]]))]
            response = discord.Embed(title="메뉴 추천", description=f'오늘은 {result}를 먹어보는 게 어떨까요?', color=helper.EMBED_COLOR)
            await ctx.send(embed=response)
        else:
            await ctx.send(embed=helper.menu_helper())


@app.command(aliases=['lotto'])
async def 로또(ctx):
    context = crawler.lotto()
    response = discord.Embed(color=helper.EMBED_COLOR)
    response.add_field(name='무기', value=f"{context['w_t_name']}\n{int(context['w_t_ticket']):,}장\n남은 시간: {context['w_t_remain']}", inline=True)
    response.add_field(name='방어구', value=f"{context['a_t_name']}\n{int(context['a_t_ticket']):,}장\n남은 시간: {context['a_t_remain']}", inline=True)
    await ctx.send(embed=response)


@app.command(aliases=['로또무기', '무기'])
async def lt(ctx):
    context = crawler.lotto()
    response = discord.Embed(color=helper.EMBED_COLOR)
    response.add_field(name='무기', value=f"{context['w_t_name']}\n{int(context['w_t_ticket']):,}장\n남은 시간: {context['w_t_remain']}", inline=True)
    response.add_field(name='어제자 무기', value=f"{context['w_y_name']}\n{context['w_y_winner']}")
    await ctx.send(embed=response)


@app.command(aliases=['로또방어구', '방어구'])
async def la(ctx):
    context = crawler.lotto()
    response = discord.Embed(color=helper.EMBED_COLOR)
    response.add_field(name='방어구', value=f"{context['a_t_name']}\n{int(context['a_t_ticket']):,}장\n남은 시간: {context['a_t_remain']}", inline=True)
    response.add_field(name='어제자 방어구', value=f"{context['a_y_name']}\n{context['a_y_winner']}")
    await ctx.send(embed=response)


# 로또결과 공지용
@tasks.loop(seconds=30)
async def lotto_result():
    now = datetime.datetime.now()
    # if True:
    if now.hour in [0, 12] and now.minute == 0 and 30 <= now.second < 60:
        response = discord.Embed(color=helper.EMBED_COLOR)
        context = crawler.lotto()
        response.add_field(name='무기', value=f"{context['w_t_name']}\n{int(context['w_t_ticket']):,}장", inline=True)
        response.add_field(name='방어구', value=f"{context['a_t_name']}\n{int(context['a_t_ticket']):,}장", inline=True)
        # 무기시간(오전9시)
        if now.hour == 0:
            response.add_field(name='어제자 무기', value=f"{context['w_y_name']}\n{context['w_y_winner']}", inline=True)
            response.add_field(name='오늘의 요일 버프', value=f'{weekday_attribute()} 피해가 10% 증가합니다', inline=False)
        else:
            response.add_field(name='어제자 방어구', value=f"{context['a_y_name']}\n{context['a_y_winner']}", inline=True)

        # await app.get_channel(876483410590310440).send(embed=response)  # 헨번방 general
        await app.get_channel(881222372898795580).send(embed=response)  # 테스트용 채널


@app.command(aliases=['속성', '요일'])
async def 요일속성(ctx):
    response = discord.Embed(color=helper.EMBED_COLOR)
    response.add_field(name='오늘의 요일 버프', value=f'{weekday_attribute()} 피해가 10% 증가합니다', inline=False)
    await ctx.send(embed=response)


def weekday_attribute():
    weekday = datetime.date.today().weekday()
    if weekday == 0:
        return '암흑'
    elif weekday == 1:
        return '불'
    elif weekday == 2:
        return '얼음'
    elif weekday == 3:
        return '바람'
    elif weekday == 4:
        return '모든'
    elif weekday == 5:
        return '전기'
    else:
        return '신성'


@lotto_result.before_loop
async def before_loop():
    await app.wait_until_ready()


@app.command(aliases=['해스', '헤스'])
async def hath(ctx, *action):
    if len(action) == 0:
        context = crawler.orderbook('hath')
        response = discord.Embed(color=helper.EMBED_COLOR)
        response.add_field(name='현재 시세', value=f"구매 최고가: {context['ask_list'][0][0]:,}c\n판매 최고가: {context['bid_list'][0][0]:,}c\n최근 거래가: {context['recent']:,}c", inline=True)
        response.add_field(name='최근 8시간', value=f"거래 최고가: {context['8h_stats'][0]:,}c\n거래 최저가: {context['8h_stats'][1]:,}c\n거래 평균가: {context['8h_stats'][2]:,}c", inline=True)
        response.add_field(name='최근 24시간', value=f"거래 최고가: {context['24h_stats'][0]:,}c\n거래 최저가: {context['24h_stats'][1]:,}c\n거래 평균가: {context['24h_stats'][2]:,}c", inline=True)
        await ctx.send(embed=response)
    elif len(action) == 2:
        if action[0] not in ['buy', 'sell'] or not action[1].isdigit():
            return
        context = crawler.orderbook('hath')
        if action[0] == 'buy':
            price_table = context['ask_list']
            amount = int(action[1])
            am, pr = amount, 0
            for pair in price_table:
                if am >= pair[1]:
                    am -= pair[1]
                    pr += pair[1] * pair[0]
                else:
                    pr += pair[0] * am
                    am = 0
                    break
            response = discord.Embed(color=helper.EMBED_COLOR)
            response.add_field(name=f'{amount:,}해스를 사기 위해서는...', value=f'{pr:,}c가 필요합니다', inline=False)
            await ctx.send(embed=response)
        elif action[0] == 'sell':
            price_table = context['bid_list']
            amount = int(action[1])
            am, pr = amount, 0
            for pair in price_table:
                if am >= pair[1]:
                    am -= pair[1]
                    pr += pair[1] * pair[0]
                else:
                    pr += pair[0] * am
                    am = 0
                    break
            pr_after_fee = int(pr * 0.99)
            response = discord.Embed(color=helper.EMBED_COLOR)
            response.add_field(name=f'{amount:,}해스를 팔면...', value=f'{pr_after_fee:,}c(1% 수수료 미포함시 {pr:,}c를 벌 수 있습니다', inline=False)
            await ctx.send(embed=response)


@app.command(aliases=['지피'])
async def gp(ctx, *action):
    if len(action) == 0:
        context = crawler.orderbook('gp')
        response = discord.Embed(color=helper.EMBED_COLOR)
        response.add_field(name='현재 시세', value=f"구매 최고가: {context['ask_list'][0][0]}c\n판매 최고가: {context['bid_list'][0][0]}c\n최근 거래가: {context['recent']}c", inline=True)
        response.add_field(name='최근 8시간', value=f"거래 최고가: {context['8h_stats'][0]}c\n거래 최저가: {context['8h_stats'][1]}c\n거래 평균가: {context['8h_stats'][2]}c", inline=True)
        response.add_field(name='최근 24시간', value=f"거래 최고가: {context['24h_stats'][0]}c\n거래 최저가: {context['24h_stats'][1]}c\n거래 평균가: {context['24h_stats'][2]}c", inline=True)
        await ctx.send(embed=response)
    elif len(action) == 2:
        if action[0] not in ['buy', 'sell'] or not action[1].isdigit():
            return
        context = crawler.orderbook('gp')
        if action[0] == 'buy':
            price_table = context['ask_list']
            amount = int(action[1])
            am, pr = amount, 0
            for pair in price_table:
                if am >= pair[1]:
                    am -= pair[1]
                    pr += pair[1] * pair[0]
                else:
                    pr += pair[0] * am
                    am = 0
                    break
            response = discord.Embed(color=helper.EMBED_COLOR)
            response.add_field(name=f'{amount:,}kGP를 사기 위해서는...', value=f'{pr:,}c가 필요합니다', inline=False)
            await ctx.send(embed=response)
        elif action[0] == 'sell':
            price_table = context['bid_list']
            amount = int(action[1])
            am, pr = amount, 0
            for pair in price_table:
                if am >= pair[1]:
                    am -= pair[1]
                    pr += pair[1] * pair[0]
                else:
                    pr += pair[0] * am
                    am = 0
                    break
            pr_after_fee = int(pr * 0.99)
            response = discord.Embed(color=helper.EMBED_COLOR)
            response.add_field(name=f'{amount:,}kGP를 팔면...', value=f'{pr_after_fee:,}c(1% 수수료 미포함시 {pr:,}c를 벌 수 있습니다', inline=False)
            await ctx.send(embed=response)


@app.event
async def on_message(message):
    if any(bad_word in message.content.lower() for bad_word in helper.BAN_WORDS) and any(exception not in message.content.lower() for exception in helper.BAN_EXCEPTIONS):
        await message.channel.send(f'{message.author.mention} - 금지어 사용에 주의해주세요', delete_after=3)
        await message.delete()
    else
        await app.process_commands(message)


lotto_result.start()
app.run(secrets['BOT']['token'])
