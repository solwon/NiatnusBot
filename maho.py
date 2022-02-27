import nextcord

from nextcord import Interaction
from nextcord.ext import commands

token = 'OTQ3NDY2ODcxMjE1NjI0MjQz.YhtrSQ.OIJ4NvlMv47Ol6KSCgGbq9iBB3I'
bot = commands.Bot(command_prefix='!')


@bot.slash_command(guild_ids=[416174233409028096])
async def 마호마호(interaction: Interaction):
    await interaction.response.send_message('hello, world!')

bot.run(token)
