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
from nextcord import Interaction

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
    await app.change_presence(status=nextcord.Status.online, activity=nextcord.Game('!도움말'))


@app.command()
async def 도움말(ctx):
    response = nextcord.Embed(title='니앗누스봇 매뉴얼', description='기능 관련 문의는 쿠루링빵에게', color=helper.EMBED_COLOR)
    response.add_field(name='UTC 0시(한국시간 9시)', value='새로운 무기와 방어구, 어제자 무기 로또 정보를 출력합니다', inline=False)
    response.add_field(name='UTC 12시(한국시간 21시)', value='무기와 새로운 방어구, 어제자 방어구 로또 정보를 출력합니다', inline=False)
    response.add_field(name='!lotto, !로또', value='무기와 방어구 로또 품목, 판매 수량, 남은 시간을 출력합니다', inline=False)
    response.add_field(name='!lt, !로또무기, !무기', value='오늘자 무기 로또 정보와 어제자 우승자를 출력합니다', inline=False)
    response.add_field(name='!la, !로또방어구, !방어구', value='오늘자 방어구 로또 정보와 어제자 우승자를 출력합니다', inline=False)
    response.add_field(name='!요일, !속성, !요일속성', value='오늘의 버프 속성을 출력하며 적 아군 상관 없이 해당 속성 저항이 감소합니다', inline=False)
    response.add_field(name='!해스, !헤스, !hath <buy/삼/sell/팜/팖> <수량>', value='아무런 인수가 없을 경우 시세 정보를, 거래 종류와 수량을 함꼐 입력 시 비용 예상을 해 줍니다', inline=False)
    response.add_field(name='!지피, !gp <buy/삼/sell/팜/팖> <수량>', value='해스 대신 GP로 같은 기능을 합니다', inline=False)
    response.add_field(name='!노래추가 <유튜브 링크>', value='데이터베이스에 유튜브 주소를 등록합니다', inline=False)
    response.add_field(name='!노래추천', value='저장된 노래 중 무작위 한 곡을 뽑아옵니다', inline=False)
    response.add_field(name='!유네뾰이', value='헨번방의 아이돌 캐릭터 가챠를 돌립니다. 당신도 1% 행운의 소유자!', inline=False)
    response.add_field(name='!가챠통계 (회원 멘션)', value='멘션 없이 호출할 경우 자신의 유네뾰이 통계를, 멘션이 있으면 멘션한 사람의 통계를 출력합니다', inline=False)
    await ctx.send(embed=response)


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
            response = nextcord.Embed(title="메뉴 추천", description=f'오늘은 {result}{helper.eulreul(result)} 먹어보는 게 어떨까요?', color=helper.EMBED_COLOR)
            await ctx.send(embed=response)
        elif cat[0] in ['특식', '찌개', '밥', '면', '국', '간편식']:
            result = foods[cat[0]][random.randrange(0, len(foods[cat[0]]))]
            response = nextcord.Embed(title="메뉴 추천", description=f'오늘은 {result}{helper.eulreul(result)} 먹어보는 게 어떨까요?', color=helper.EMBED_COLOR)
            await ctx.send(embed=response)
        else:
            await ctx.send(embed=helper.menu_helper())


@app.command(aliases=['lotto'])
async def 로또(ctx):
    context = crawler.lotto()
    response = nextcord.Embed(color=helper.EMBED_COLOR)
    response.add_field(name='무기', value=f"{context['w_t_name']}\n{int(context['w_t_ticket']):,}장\n남은 시간: {context['w_t_remain']}", inline=True)
    response.add_field(name='방어구', value=f"{context['a_t_name']}\n{int(context['a_t_ticket']):,}장\n남은 시간: {context['a_t_remain']}", inline=True)
    await ctx.send(embed=response)


@app.command(aliases=['로또무기', '무기'])
async def lt(ctx):
    context = crawler.lotto()
    response = nextcord.Embed(color=helper.EMBED_COLOR)
    response.add_field(name='무기', value=f"{context['w_t_name']}\n{int(context['w_t_ticket']):,}장\n남은 시간: {context['w_t_remain']}", inline=True)
    response.add_field(name='어제자 무기', value=f"{context['w_y_name']}\n{int(context['w_y_ticket']):,}장\n{context['w_y_winner']}")
    await ctx.send(embed=response)


@app.command(aliases=['로또방어구', '방어구'])
async def la(ctx):
    context = crawler.lotto()
    response = nextcord.Embed(color=helper.EMBED_COLOR)
    response.add_field(name='방어구', value=f"{context['a_t_name']}\n{int(context['a_t_ticket']):,}장\n남은 시간: {context['a_t_remain']}", inline=True)
    response.add_field(name='어제자 방어구', value=f"{context['a_y_name']}\n{int(context['a_y_ticket']):,}장\n{context['a_y_winner']}")
    await ctx.send(embed=response)


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


@app.command(aliases=['속성', '요일'])
async def 요일속성(ctx):
    response = nextcord.Embed(color=helper.EMBED_COLOR)
    attribute = weekday_attribute()
    response.add_field(name='오늘의 요일 버프', value=f'{attribute[0]} 저항이 {attribute[1]}% 감소합니다', inline=False)
    await ctx.send(embed=response)


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


@app.command(aliases=['해스', '헤스'])
async def hath(ctx, *action):
    if len(action) == 0:
        context = crawler.orderbook('hath')
        response = nextcord.Embed(color=helper.EMBED_COLOR)
        response.add_field(name='현재 시세', value=f"매수 최고가: {context['ask_list'][0][0]:,}c\n매도 최저가: {context['bid_list'][0][0]:,}c\n최근 거래가: {context['recent']:,}c", inline=True)
        response.add_field(name='최근 8시간', value=f"거래 최고가: {context['8h_stats'][0]:,}c\n거래 최저가: {context['8h_stats'][1]:,}c\n거래 평균가: {context['8h_stats'][2]:,}c", inline=True)
        response.add_field(name='최근 24시간', value=f"거래 최고가: {context['24h_stats'][0]:,}c\n거래 최저가: {context['24h_stats'][1]:,}c\n거래 평균가: {context['24h_stats'][2]:,}c", inline=True)
        await ctx.send(embed=response)
    elif len(action) == 2:
        if action[0] not in ['buy', 'sell', '삼', '팜', '팖'] or not action[1].isdigit():
            return
        elif int(action[1]) == 0:
            return
        context = crawler.orderbook('hath')
        if action[0] in ['buy', '삼']:
            response = nextcord.Embed(color=helper.EMBED_COLOR)
            price_table = context['ask_list']
            amount = int(action[1])
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
                response.add_field(name=f'{amount:,}해스를 사기 위해서는...', value=f'{pr:,}c가 필요합니다', inline=False)
            else:
                response.add_field(name=f'{amount:,}해스를 살 수 없습니다', value=f'{am_max:,}해스를 {pr_max:,}c에 살 수 있지만 그 이상은 매도 주문이 부족합니다.', inline=False)
            await ctx.send(embed=response)
        elif action[0] in ['sell', '팜', '팖']:
            response = nextcord.Embed(color=helper.EMBED_COLOR)
            price_table = context['bid_list']
            amount = int(action[1])
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
                response.add_field(name=f'{amount:,}해스를 팔면...', value=f'{pr_after_fee:,}c(1% 수수료 미포함 시 {pr:,}c)를 벌 수 있습니다', inline=False)
            else:
                pr_after_fee = int(pr_max * 0.99)
                response.add_field(name=f'{amount:,}해스를 팔 수 없습니다', value=f'{am_max:,}해스를 팔아 {pr_after_fee:,}c(1% 수수료 미포함 시 {pr_max:,}c)를 벌 수 있지만 그 이상은 매수 주문이 부족합니다.', inline=False)
            await ctx.send(embed=response)


@app.command(aliases=['지피'])
async def gp(ctx, *action):
    if len(action) == 0:
        context = crawler.orderbook('gp')
        response = nextcord.Embed(color=helper.EMBED_COLOR)
        response.add_field(name='현재 시세', value=f"매수 최고가: {context['ask_list'][0][0]}c\n매도 최저가: {context['bid_list'][0][0]}c\n최근 거래가: {context['recent']}c", inline=True)
        response.add_field(name='최근 8시간', value=f"거래 최고가: {context['8h_stats'][0]}c\n거래 최저가: {context['8h_stats'][1]}c\n거래 평균가: {context['8h_stats'][2]}c", inline=True)
        response.add_field(name='최근 24시간', value=f"거래 최고가: {context['24h_stats'][0]}c\n거래 최저가: {context['24h_stats'][1]}c\n거래 평균가: {context['24h_stats'][2]}c", inline=True)
        await ctx.send(embed=response)
    elif len(action) == 2:
        if action[0] not in ['buy', 'sell', '삼', '팜', '팖'] or not action[1].isdigit():
            return
        elif int(action[1]) == 0:
            return
        context = crawler.orderbook('gp')
        if action[0] in ['buy', '삼']:
            response = nextcord.Embed(color=helper.EMBED_COLOR)
            price_table = context['ask_list']
            amount = int(action[1])
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
                response.add_field(name=f'{amount:,}kGP를 사기 위해서는...', value=f'{pr:,}c가 필요합니다', inline=False)
            else:
                response.add_field(name=f'{amount:,}kGP를 살 수 없습니다',
                                   value=f'{am_max:,}kGP를 {pr_max:,}c에 살 수 있지만 그 이상은 매도 주문이 부족합니다.', inline=False)
            await ctx.send(embed=response)
        elif action[0] in ['sell', '팜', '팖']:
            response = nextcord.Embed(color=helper.EMBED_COLOR)
            price_table = context['bid_list']
            amount = int(action[1])
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
                response.add_field(name=f'{amount:,}kGP를 팔면...',
                                   value=f'{pr_after_fee:,}c(1% 수수료 미포함 시 {pr:,}c)를 벌 수 있습니다', inline=False)
            else:
                pr_after_fee = int(pr_max * 0.99)
                response.add_field(name=f'{amount:,}kGP를 팔 수 없습니다',
                                   value=f'{am_max:,}kGP를 팔아 {pr_after_fee:,}c(1% 수수료 미포함 시 {pr_max:,}c)를 벌 수 있지만 그 이상은 매수 주문이 부족합니다.',
                                   inline=False)
            await ctx.send(embed=response)


@app.command(aliases=['\유네뾰이', '유\네뾰이', '유네\뾰이', '유네뾰\이', '유네뵤이'])
async def 유네뾰이(ctx):
    # response = nextcord.Embed(color=helper.EMBED_COLOR)
    # response.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    userid = ctx.author.id
    username = ctx.author.display_name
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
        response.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
        await ctx.send(message, embed=response)
    else:
        # await ctx.send(f'{ctx.author.mention} 쿨타임입니다', delete_after=1)
        await ctx.message.delete()


@app.command()
async def 구통계(ctx, *args):
    is_error = False
    if len(args) == 0:
        userid = ctx.author.id
        username = ctx.author.display_name
    elif len(args) == 1:
        if helper.is_mention(args[0]):
            userid = ctx.message.mentions[0].id
            username = ctx.message.mentions[0].display_name
        else:
            is_error = True
    else:
        is_error = True
    if is_error:
        print(len(args), ctx.message.content)
        description = f'```\n가챠통계 (원하는 사람 멘션) 의 형태로 써 주세요\n```'
        await ctx.reply(description)
    else:
        result = niatnusdb.gacha_stats(userid, username, 1)
        description = f'```\n{username}님은 {result.count}만큼 유네뾰이 시즌 1을 사랑해요!\n★☆☆☆☆☆ | {result.star_1}\n★★☆☆☆☆ | {result.star_2}\n★★★☆☆☆ | {result.star_3}\n★★★★☆☆ | {result.star_4}\n★★★★★☆ | {result.star_5}\n★★★★★★ | {result.star_6}\n```'
        await ctx.send(description)


@app.command(aliases=['가차통계'])
async def 가챠통계(ctx, *args):
    is_error = False
    if len(args) == 0:
        userid = ctx.author.id
        username = ctx.author.display_name
    elif len(args) == 1:
        if helper.is_mention(args[0]):
            userid = ctx.message.mentions[0].id
            username = ctx.message.mentions[0].display_name
        else:
            is_error = True
    else:
        is_error = True
    if is_error:
        print(len(args), ctx.message.content)
        description = f'```\n가챠통계 (원하는 사람 멘션) 의 형태로 써 주세요\n```'
        await ctx.reply(description)
    else:
        result = niatnusdb.gacha_stats(userid, username, 2)
        description = f'```\n{username}님은 {result.count}만큼 유네뾰이 시즌 2를 사랑해요!\n★☆☆☆☆☆ | {result.star_1}\n★★☆☆☆☆ | {result.star_2}\n★★★☆☆☆ | {result.star_3}\n★★★★☆☆ | {result.star_4}\n★★★★★☆ | {result.star_5}\n★★★★★★ | {result.star_6}\n```'
        await ctx.send(description)


@app.command()
async def 노래추가(ctx, url):
    validation = helper.youtube_validation(url)
    if not validation[0]:
        await ctx.send(f'{ctx.author.mention} 올바른 유튜브 주소형식이 아닙니다', delete_after=3)
        await ctx.message.delete()
    else:
        userid = ctx.author.id
        username = ctx.author.display_name
        result = niatnusdb.add_ducksong(url, userid, username)
        if result:
            await ctx.send(f'{ctx.author.mention} 해당 노래가 추가되었습니다.')
        else:
            await ctx.send(f'{ctx.author.mention} 이미 추가된 노래입니다.')


@app.command()
async def 노래추천(ctx):
    result = niatnusdb.get_ducksong()
    await ctx.send(f'{result}')


@app.slash_command(name='testnistnus', guild_ids=[782997633328611438])
async def nistnustest(interaction: Interaction):
    await interaction.response.send_message('hello, world!')


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
