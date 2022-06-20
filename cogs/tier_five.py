import disnake

from disnake.ext import commands
from disnake.ext.commands import Cog


class TierFiveCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    # DND PL and DND DM commands



def setup(bot):
    bot.add_cog(TierFiveCommands(bot))