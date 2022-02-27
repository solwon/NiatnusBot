import asyncio
import random
import nextcord
import json
import datetime

import crawler
import helper
import niatnusdb

from nextcord.ext import commands, tasks
from nextcord.ext.commands import CommandNotFound
from nextcord import Interaction, SlashOption

intents = nextcord.Intents.default()
app = commands.Bot(command_prefix='!', intents=intents)
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
    await app.change_presence(status=nextcord.Status.online, activity=nextcord.Game('아무 것도 안'))


# @app.slash_command(guild_ids=[secrets['DISCORD']['server']])
# async def 도움말(interaction: Interaction):
#     response = nextcord.Embed(title='니앗누스봇 매뉴얼', description='기능 관련 문의는 쿠루링빵에게', color=helper.EMBED_COLOR)
#     response.add_field(name='UTC 0시(한국시간 9시)', value='새로운 무기와 방어구, 어제자 무기 로또 정보를 출력합니다', inline=False)
#     response.add_field(name='UTC 12시(한국시간 21시)', value='무기와 새로운 방어구, 어제자 방어구 로또 정보를 출력합니다', inline=False)
#     response.add_field(name='/lotto, /로또', value='무기와 방어구 로또 품목, 판매 수량, 남은 시간을 출력합니다', inline=False)
#     response.add_field(name='/lt, /로또무기, /무기', value='오늘자 무기 로또 정보와 어제자 우승자를 출력합니다', inline=False)
#     response.add_field(name='/la, /로또방어구, /방어구', value='오늘자 방어구 로또 정보와 어제자 우승자를 출력합니다', inline=False)
#     response.add_field(name='/요일, /속성, /요일속성', value='오늘의 버프 속성을 출력하며 적 아군 상관 없이 해당 속성 저항이 감소합니다', inline=False)
#     response.add_field(name='/해스, /헤스, /hath <buy/삼/sell/팜/팖> <수량>', value='아무런 인수가 없을 경우 시세 정보를, 거래 종류와 수량을 함꼐 입력 시 비용 예상을 해 줍니다', inline=False)
#     response.add_field(name='/지피, /gp <buy/삼/sell/팜/팖> <수량>', value='해스 대신 GP로 같은 기능을 합니다', inline=False)
#     response.add_field(name='/노래추가 <유튜브 링크>', value='데이터베이스에 유튜브 주소를 등록합니다', inline=False)
#     response.add_field(name='/노래추천', value='저장된 노래 중 무작위 한 곡을 뽑아옵니다', inline=False)
#     response.add_field(name='/유네뾰이', value='헨번방의 아이돌 캐릭터 가챠를 돌립니다. 당신도 1% 행운의 소유자!', inline=False)
#     response.add_field(name='/가챠통계 (회원 멘션)', value='멘션 없이 호출할 경우 자신의 유네뾰이 통계를, 멘션이 있으면 멘션한 사람의 통계를 출력합니다', inline=False)
#     await interaction.response.send_message(embed=response)


@app.slash_command(guild_ids=[secrets['DISCORD']['server']], description='니앗누스에게 식사 메뉴를 추천받습니다')
async def 뭐먹지(interaction: Interaction, arg: str = SlashOption(name='음식 종류', description='선택할 음식의 종류', choices={'특식': '특식', '찌개': '찌개', '밥': '밥', '면': '면', '국': '국', '간편식': '간편식'})):
    if not arg:
        await interaction.response.send_message(embed=helper.menu_helper())
    else:
        if arg == '전부':
            menus = []
            for k, v in foods.items():
                menus += v
            result = menus[random.randrange(0, len(menus))]
            response = nextcord.Embed(title="메뉴 추천", description=f'오늘은 {result}{helper.eulreul(result)} 먹어보는 게 어떨까요?', color=helper.EMBED_COLOR)
            await interaction.response.send_message(embed=response)
        elif arg in ['특식', '찌개', '밥', '면', '국', '간편식']:
            result = foods[arg][random.randrange(0, len(foods[arg]))]
            response = nextcord.Embed(title="메뉴 추천", description=f'오늘은 {result}{helper.eulreul(result)} 먹어보는 게 어떨까요?', color=helper.EMBED_COLOR)
            await interaction.response.send_message(embed=response)
        else:
            await interaction.response.send_message(embed=helper.menu_helper())


@app.slash_command(guild_ids=[secrets['DISCORD']['server']], description='오늘의 로또 요약을 봅니다')
async def 로또(interaction: Interaction):
    context = crawler.lotto()
    response = nextcord.Embed(color=helper.EMBED_COLOR)
    response.add_field(name='무기', value=f"{context['w_t_name']}\n{int(context['w_t_ticket']):,}장\n남은 시간: {context['w_t_remain']}", inline=True)
    response.add_field(name='방어구', value=f"{context['a_t_name']}\n{int(context['a_t_ticket']):,}장\n남은 시간: {context['a_t_remain']}", inline=True)
    await interaction.response.send_message(embed=response)


@app.slash_command(guild_ids=[secrets['DISCORD']['server']], description='오늘의 무기 로또 정보를 봅니다')
async def 무기(interaction: Interaction):
    context = crawler.lotto()
    response = nextcord.Embed(color=helper.EMBED_COLOR)
    response.add_field(name='무기', value=f"{context['w_t_name']}\n{int(context['w_t_ticket']):,}장\n남은 시간: {context['w_t_remain']}", inline=True)
    response.add_field(name='어제자 무기', value=f"{context['w_y_name']}\n{int(context['w_y_ticket']):,}장\n{context['w_y_winner']}")
    await interaction.response.send_message(embed=response)


@app.slash_command(guild_ids=[secrets['DISCORD']['server']], description='오늘의 방어구 로또 정보를 봅니다')
async def 방어구(interaction: Interaction):
    context = crawler.lotto()
    response = nextcord.Embed(color=helper.EMBED_COLOR)
    response.add_field(name='방어구', value=f"{context['a_t_name']}\n{int(context['a_t_ticket']):,}장\n남은 시간: {context['a_t_remain']}", inline=True)
    response.add_field(name='어제자 방어구', value=f"{context['a_y_name']}\n{int(context['a_y_ticket']):,}장\n{context['a_y_winner']}")
    await interaction.response.send_message(embed=response)


# 로또결과 공지용
@tasks.loop(seconds=30)
async def lotto_result():
    now = datetime.datetime.now()
    # if True:
    if now.hour in [0, 12] and now.minute == 0 and 30 <= now.second < 60:
        response = nextcord.Embed(color=helper.EMBED_COLOR)
        context = crawler.lotto()
        response.add_field(name='무기', value=f"{context['w_t_name']}\n{int(context['w_t_ticket']):,}장", inline=True)
        response.add_field(name='방어구', value=f"{context['a_t_name']}\n{int(context['a_t_ticket']):,}장", inline=True)
        # 무기시간(오전9시)
        if now.hour == 0:
            attribute = weekday_attribute()
            response.add_field(name='어제자 무기', value=f"{context['w_y_name']}\n{int(context['w_y_ticket']):,}장\n{context['w_y_winner']}", inline=True)
            response.add_field(name='오늘의 요일 버프', value=f'{attribute[0]} 저항이 {attribute[1]}% 감소합니다', inline=False)
        else:
            response.add_field(name='어제자 방어구', value=f"{context['a_y_name']}\n{int(context['a_y_ticket']):,}장\n{context['a_y_winner']}", inline=True)

        sys_chan = app.get_guild(secrets['DISCORD']['server']).system_channel
        if not sys_chan:
            await app.get_guild(secrets['DISCORD']['server']).get_channel(secrets['DISCORD']['bot_command']).send(f"{secrets['GACHA']['goom']} 시스템 채널을 확인해주세요")
        else:
            await app.get_guild(secrets['DISCORD']['server']).system_channel.send(embed=response) # 헨번방 general
        # await app.get_channel(secrets['DISCORD']['test_channel']).send(embed=response)  # 테스트용 채널


@app.slash_command(guild_ids=[secrets['DISCORD']['server']], description='오늘의 속성 정보를 봅니다')
async def 속성(interaction: Interaction):
    response = nextcord.Embed(color=helper.EMBED_COLOR)
    attribute = weekday_attribute()
    response.add_field(name='오늘의 요일 버프', value=f'{attribute[0]} 저항이 {attribute[1]}% 감소합니다', inline=False)
    await interaction.response.send_message(embed=response)


def weekday_attribute():
    weekday = datetime.date.today().weekday()
    if weekday == 0:
        return '암흑', 10
    elif weekday == 1:
        return '불', 10
    elif weekday == 2:
        return '얼음', 10
    elif weekday == 3:
        return '바람', 10
    elif weekday == 4:
        return '속성, 보이드, 베기, 관통, 타격', 5
    elif weekday == 5:
        return '전기', 10
    else:
        return '신성', 10


@lotto_result.before_loop
async def before_loop():
    await app.wait_until_ready()


@app.slash_command(guild_ids=[secrets['DISCORD']['server']], description='해스 시세 정보를 봅니다')
async def 해스(interaction: Interaction):
    pass


@해스.subcommand(description='현재 시세 정보')
async def 시세(interaction: Interaction):
    response = orderbook('hath')
    await interaction.response.send_message(embed=response)


@해스.subcommand(description='해스 판매 계산기')
async def 팜(interaction: Interaction, amount: int = SlashOption(name='수량', description='판매할 수량 입력(최대 50000해스)', required=True, min_value=0, max_value=50000)):
    response = market_calc('hath', 'buy', amount)
    if response:
        await interaction.response.send_message(embed=response)


@해스.subcommand(description='해스 구매 계산기')
async def 삼(interaction: Interaction, amount: int = SlashOption(name='수량', description='구매할 수량 입력(최대 50000해스)', required=True, min_value=0, max_value=50000)):
    response = market_calc('hath', 'sell', amount)
    if response:
        await interaction.response.send_message(embed=response)


@app.slash_command(guild_ids=[secrets['DISCORD']['server']], description='GP 시세 정보를 봅니다')
async def 지피(interaction: Interaction):
    pass


@지피.subcommand(description='현재 시세 정보')
async def 시세(interaction: Interaction):
    response = orderbook('gp')
    await interaction.response.send_message(embed=response)


@지피.subcommand(description='GP 판매 계산기')
async def 팜(interaction: Interaction, amount: int = SlashOption(name='수량', description='판매할 수량 입력(최대 50000kGP)', required=True, min_value=0, max_value=50000)):
    response = market_calc('gp', 'buy', amount)
    if response:
        await interaction.response.send_message(embed=response)


@지피.subcommand(description='GP 구매 계산기')
async def 삼(interaction: Interaction, amount: int = SlashOption(name='수량', description='구매할 수량 입력(최대 50000kGP)', required=True, min_value=0, max_value=50000)):
    response = market_calc('gp', 'sell', amount)
    if response:
        await interaction.response.send_message(embed=response)


def orderbook(currency):
    context = crawler.orderbook('currency')
    response = nextcord.Embed(color=helper.EMBED_COLOR)
    response.add_field(name='현재 시세', value=f"매수 최고가: {context['ask_list'][0][0]:,}c\n매도 최저가: {context['bid_list'][0][0]:,}c\n최근 거래가: {context['recent']:,}c", inline=True)
    response.add_field(name='최근 8시간', value=f"거래 최고가: {context['8h_stats'][0]:,}c\n거래 최저가: {context['8h_stats'][1]:,}c\n거래 평균가: {context['8h_stats'][2]:,}c", inline=True)
    response.add_field(name='최근 24시간', value=f"거래 최고가: {context['24h_stats'][0]:,}c\n거래 최저가: {context['24h_stats'][1]:,}c\n거래 평균가: {context['24h_stats'][2]:,}c", inline=True)
    return response


def market_calc(currency, action, amount):
    curr_str = '해스' if currency == 'hath' else 'kGP'
    if amount == 0:
        return
    context = crawler.orderbook(currency)
    if action == 'buy':
        response = nextcord.Embed(color=helper.EMBED_COLOR)
        price_table = context['ask_list']
        am_max, pr_max = sum([pair[1] for pair in price_table]), sum([pair[0] * pair[1] for pair in price_table])
        am, pr = amount, 0
        if amount <= am_max:
            for pair in price_table:
                if am >= pair[1]:
                    am -= pair[1]
                    pr += pair[1] * pair[0]
                else:
                    pr += pair[0] * am
                    am = 0
                    break
            response.add_field(name=f'{amount:,}{curr_str}를 사기 위해서는...', value=f'{pr:,}c가 필요합니다', inline=False)
        else:
            response.add_field(name=f'{amount:,}{curr_str}를 살 수 없습니다',
                               value=f'{am_max:,}{curr_str}를 {pr_max:,}c에 살 수 있지만 그 이상은 매도 주문이 부족합니다.', inline=False)
        return response
    elif action == 'sell':
        response = nextcord.Embed(color=helper.EMBED_COLOR)
        price_table = context['bid_list']
        am_max, pr_max = sum([pair[1] for pair in price_table]), sum([pair[0] * pair[1] for pair in price_table])
        if amount <= am_max:
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
            response.add_field(name=f'{amount:,}{curr_str}를 팔면...', value=f'{pr_after_fee:,}c(1% 수수료 미포함 시 {pr:,}c)를 벌 수 있습니다',
                               inline=False)
        else:
            pr_after_fee = int(pr_max * 0.99)
            response.add_field(name=f'{amount:,}{curr_str}를 팔 수 없습니다',
                               value=f'{am_max:,}{curr_str}를 팔아 {pr_after_fee:,}c(1% 수수료 미포함 시 {pr_max:,}c)를 벌 수 있지만 그 이상은 매수 주문이 부족합니다.',
                               inline=False)
        return response


@app.slash_command(guild_ids=[secrets['DISCORD']['server']], description='헨번방의 아이돌 가챠!')
async def 유네뾰이(interaction: Interaction):
    # response = nextcord.Embed(color=helper.EMBED_COLOR)
    # response.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    userid = interaction.user.id
    username = interaction.user.display_name
    result = niatnusdb.check_gacha_cd(userid, username)
    if result:
        message = ''
        if result == -1:
            response = nextcord.Embed(title='밴 대상입니다', description='그러게 처신을 잘 했어야지', color=helper.EMBED_COLOR)
        elif result == 1:
            response = nextcord.Embed(title=f'★', color=helper.EMBED_COLOR)
            response.set_image(url=secrets['GACHA']['1'])
        elif result == 2:
            response = nextcord.Embed(title=f'★★', color=helper.EMBED_COLOR)
            response.set_image(url=secrets['GACHA']['2'])
        elif result == 3:
            response = nextcord.Embed(title=f'★★★', color=helper.EMBED_COLOR)
            response.set_image(url=secrets['GACHA']['3'])
        elif result == 4:
            response = nextcord.Embed(title=f'★★★★', color=helper.EMBED_COLOR)
            response.set_image(url=secrets['GACHA']['4'])
        elif result == 5:
            message = secrets['GACHA']['yunetsun']
            response = nextcord.Embed(title=f'★★★★★', color=helper.EMBED_COLOR)
            response.set_image(url=secrets['GACHA']['5'])
        else:
            message = secrets['GACHA']['yunetsun']
            response = nextcord.Embed(title=f'★★★★★★', color=helper.EMBED_COLOR)
            response.set_image(url=secrets['GACHA']['6'])
        response.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar)
        await interaction.response.send_message(message, embed=response)
    else:
        # await interaction.response.send_message(f'{ctx.author.mention} 쿨타임입니다', delete_after=1)
        await interaction.message.delete()


@app.slash_command(guild_ids=[secrets['DISCORD']['server']], description='과거 유네뾰이 통계를 봅니다')
async def 구통계(interaction: Interaction, user: nextcord.Member = SlashOption(name='유저', description='통계를 볼 유저명(비울시 자기 자신)', required=False)):
    if not user:
        userid = interaction.user.id
        username = interaction.user.display_name
    else:
        userid = user.id
        username = user.display_name
    result = niatnusdb.gacha_stats(userid, username, 1)
    description = f'```\n{username}님은 {result.count}만큼 유네뾰이 시즌 1을 사랑해요!\n★☆☆☆☆☆ | {result.star_1}\n★★☆☆☆☆ | {result.star_2}\n★★★☆☆☆ | {result.star_3}\n★★★★☆☆ | {result.star_4}\n★★★★★☆ | {result.star_5}\n★★★★★★ | {result.star_6}\n```'
    await interaction.response.send_message(description)


@app.slash_command(guild_ids=[secrets['DISCORD']['server']], description='유네뾰이 통계를 봅니다')
async def 가챠통계(interaction: Interaction, user: nextcord.Member = SlashOption(name='유저', description='통계를 볼 유저명(비울시 자기 자신)', required=False)):
    if not user:
        userid = interaction.user.id
        username = interaction.user.display_name
    else:
        userid = user.id
        username = user.display_name
    result = niatnusdb.gacha_stats(userid, username, 2)
    description = f'```\n{username}님은 {result.count}만큼 유네뾰이 시즌 2를 사랑해요!\n★☆☆☆☆☆ | {result.star_1}\n★★☆☆☆☆ | {result.star_2}\n★★★☆☆☆ | {result.star_3}\n★★★★☆☆ | {result.star_4}\n★★★★★☆ | {result.star_5}\n★★★★★★ | {result.star_6}\n```'
    await interaction.response.send_message(description)


# @app.command()
# async def 노래추가(ctx, url):
#     validation = helper.youtube_validation(url)
#     if not validation[0]:
#         await interaction.response.send_message(f'{ctx.author.mention} 올바른 유튜브 주소형식이 아닙니다', delete_after=3)
#         await ctx.message.delete()
#     else:
#         userid = ctx.author.id
#         username = ctx.author.display_name
#         result = niatnusdb.add_ducksong(url, userid, username)
#         if result:
#             await interaction.response.send_message(f'{ctx.author.mention} 해당 노래가 추가되었습니다.')
#         else:
#             await interaction.response.send_message(f'{ctx.author.mention} 이미 추가된 노래입니다.')
#
#
# @app.command()
# async def 노래추천(ctx):
#     result = niatnusdb.get_ducksong()
#     await interaction.response.send_message(f'{result}')


@app.slash_command(guild_ids=[secrets['DISCORD']['server']], description='지정한 유저의 프로필 사진을 봅니다')
async def avatar(interaction: Interaction, user: nextcord.Member = SlashOption(name='유저명', description='입력하지 않으면 자기 자신의 프로필 사진이 출력됩니다', required=False)):
    if not user:
        prof_picture = interaction.user.display_avatar
    else:
        prof_picture = user.display_avatar
    await interaction.response.send_message(prof_picture)


@app.event
async def on_message(message):
    if any(bad_word in message.content.lower() for bad_word in helper.BAN_WORDS) and any(exception not in message.content.lower() for exception in helper.BAN_EXCEPTIONS):
        await message.channel.send(f'{message.author.mention} - 금지어 사용에 주의해주세요', delete_after=3)
        await message.delete()
    else:
        await app.process_commands(message)


@app.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error


# @app.event
# async def on_ready():
#     print(app.get_guild(secrets['DISCORD']['server']).system_channel)
#     await app.get_guild(secrets['DISCORD']['server']).system_channel.send('시스템 채널입니다')


lotto_result.start()
app.run(secrets['BOT']['token'])
