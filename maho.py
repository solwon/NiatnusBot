import nextcord

from nextcord import Interaction, SlashOption
from nextcord.ext import commands

token = 'OTQ3NDY2ODcxMjE1NjI0MjQz.YhtrSQ.OIJ4NvlMv47Ol6KSCgGbq9iBB3I'
bot = commands.Bot(command_prefix='!')


@bot.slash_command(guild_ids=[416174233409028096])
async def 마호마호(interaction: Interaction):
    await interaction.response.send_message('hello, world!')


@bot.slash_command(guild_ids=[416174233409028096])
async def 마호티콘(interaction: Interaction, eid: str = SlashOption(name='이름', description='이모티콘 이름')):
    emojis = interaction.guild.emojis
    emojis = list(filter(lambda x: x.name == eid, emojis))
    if len(emojis) == 0:
        await interaction.response.send_message('없는 이모티콘입니다.')
    else:
        response = nextcord.Embed()
        response.set_image(url=emojis[0].url)
        response.set_author(name=interaction.user.display_name, icon_url=str(interaction.user.avatar))
        await interaction.response.send_message(embed=response)


@bot.event
async def on_message(message: nextcord.Message):
    if message.reference:
        await message.channel.send(f'{[x.name for x in message.mentions]}')
    await bot.process_commands(message)

bot.run(token)
