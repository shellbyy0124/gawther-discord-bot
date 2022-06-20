import disnake

from disnake.ext import commands
from disnake.ext.commands import Cog


class TierOneCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    # owner commands


def setup(bot):
    bot.add_cog(TierOneCommands(bot))