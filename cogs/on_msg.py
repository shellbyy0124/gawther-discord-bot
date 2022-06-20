import disnake
import sys
import os
import json
import asyncio

from disnake.ext import commands
from disnake.ext.commands import Cog


class OnMessageEvents(Cog):
    def __init__(self,bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self,message):
        if message.content.startswith('ghelpp'):
            await message.delete()
            await message.author.send(
                "To see the help menu, please type `/gen_help` for general help commands or `/staff_help` for staff help commands"
            )


def setup(bot):
    bot.add_cog(OnMessageEvents(bot))