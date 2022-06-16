import disnake
import json
import os
import sys

from disnake.ext import commands
from disnake.ext.commands import Cog

"""remove before production"""
if not os.path.isfile('config.json'):
    sys.exit("'config.json' Not Found!")
else:
    with open('./config.json','r',encoding="utf-8-sig") as f:
        data = json.load(f)

guild_id = data["bot_info"]["guild_id"]


class DeveloperCommands(Cog):
    def __init__(self, bot):
        self.bot = bot




def setup(bot):
    bot.add_cog(DeveloperCommands(bot))