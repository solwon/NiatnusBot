import asyncio
import discord
import json

from discord.ext import commands
app = commands.Bot(command_prefix='!', help_command=None)
secrets = json.loads(open('secrets.json').read())

@app.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(app.user.name)
    print('connection was succesful')
    await app.change_presence(status=discord.Status.online, activity=discord.Game("!도움"))


@app.command()
async def 도움(ctx):
    command = discord.Embed(title="명령어",description="명령어 목록", color=0x62c1cc)
    command.add_field(name="!안뇽", value="헬로 펭귄 출력", inline=False)
    command.add_field(name="!안녕", value="바이 펭귄 출력", inline=False)
    command.add_field(name="!해명해", value="해명해콘 출력", inline=False)
    command.add_field(name="!노루", value="ex)!노루 ooo > ooo를 구글 이미지 검색 후 출력", inline=False)
    command.add_field(name="!삭 or !a", value="!노루 명령어의 마지막 사진을 삭제(개발중)", inline=False)
    await ctx.send(embed=command)

app.run(secrets['BOT']['token'])