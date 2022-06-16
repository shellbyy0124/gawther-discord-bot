import disnake
import json
import os
import sys

import sqlite3 as sql

from disnake.ext import commands
from disnake.ext.commands import Cog

"""remove before production"""
if not os.path.isfile('config.json'):
    sys.exit("'config.json' Not Found!")
else:
    with open('./config.json','r',encoding="utf-8-sig") as f:
        data = json.load(f)

guild_id = data["bot_info"]["guild_id"]
"""===================================="""

with sql.connect('main.db') as mdb:
    cur = mdb.cursor()


class GeneralCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name = 'ping',
        description = "Returns Bot Latency.",
        guild_ids = [guild_id]
    )
    async def ping(self, inter):
        await inter.response.send_message(
            'Latency Returned {}ms'.format(round(self.bot.latency * 1000))
        )


    @commands.slash_command(
        name = 'server',
        description = "Returns Info About Guild",
        guild_ids = [guild_id]
    )
    async def server(self, inter):
        guild = self.bot.get_guild(guild_id)
        created_at_corrected = guild.created_at.__format__("%m/%d/%Y - %H:%M:%S")
        owner_role = disnake.utils.get(guild.roles, name="Owner")
        owners = []

        for member in guild.members:
            if owner_role in member.roles:
                owners.append(member.name)

        embed = disnake.Embed(
            color=disnake.Colour.random(),
            title="{} Server Info".format(guild.name),
            description = "Below you can find information about {}".format(guild.name)
        ).add_field(
            name="Creation Information",
            value="Created At: {}\nHead Robot: {}\nGuild Owner(s): {}".format(created_at_corrected, self.bot.user.name, ", ".join(owners)),
            inline=False
        ).add_field(
            name="Staff Roles",
            value="{}".format(", ".join(["Owner", "Head Administrator", "Administrator", "Moderator"]))
        ).add_field(
            name="Developer Roles",
            value="{}".format(", ".join(["Lead Developer", "Gawther Developer", "KasMek Developer"])),
            inline=False
        ).add_field(
            name="Designer Roles",
            value="{}".format(", ".join(["Lead Designer", "KasMek Designer", "Gawther Designer"])),
            inline=False
        ).add_field(
            name="Support Roles",
            value="{}".format(", ".join(["Head Support", "Support Staff", "Community Helper"])),
            inline=False
        ).set_thumbnail(
            url = self.bot.user.avatar
        ).set_footer(
            text="If you need further assistance, please use `>help` command."
        )

        await inter.response.send_message(
            embed=embed
        )


    @commands.slash_command(
        name="whois",
        description="Returns a profile on the user.",
        guild_ids=[guild_id]
    )
    async def whois(self, inter, member:disnake.Member=None):
        if member is None:
            member = inter.author

        srch = 'SELECT exp FROM members WHERE id=?'
        val = (member.id,)

        srch2 = 'SELECT fav_col FROM members WHERE id=?'

        user_exp = cur.execute(srch, val).fetchone()
        user_fav_color = cur.execute(srch2, val).fetchone()

        embed = disnake.Embed(
            color=disnake.Colour.random(),
            title="{}'s Profile".format(member.display_name),
            description="Below you will find various information about {}".format(member.display_name)
        ).add_field(
            name="General Information",
            value="Current Level: N/A\nCurrent Experience: {}".format(int(user_exp[0])),
            inline=False
        ).add_field(
            name="Favorite Things",
            value="Favorite Color: {}".format(user_fav_color[0]),
            inline=False
        ).set_thumbnail(
            url=member.avatar
        )

        await inter.response.send_message(
            embed=embed
        )


def setup(bot):
    bot.add_cog(GeneralCommands(bot))