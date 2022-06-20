import disnake
import sys
import os
import json

import sqlite3 as sql

from disnake.ext import commands
from disnake.ext.commands import Cog

if not os.path.isfile('config.json'):
    sys.exit("'config.json' Not Found!")
else:
    with open('./config.json','r',encoding='utf-8-sig') as f:
        data = json.load(f)


guild_id = data["bot_info"]["guild_id"]


class TierSixCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    # general commands for Developers, Designers, Nitro Members, Programming, Gaming, and Member roles

    @commands.slash_command(
        name = 'ping',
        description = "Returns Bot Latency."
    )
    @commands.has_any_role(
        "Owner", "Gawther", "Head Administrator", "Head Developer",
        "Head Designer", "Head Support", "Administrator", "Moderator",
        "Support Staff", "Community Helper", "DND_DM", "DND PL", "Developers",
        "Designers", "Nitro Member", "Programming", "Gaming", "Member"
    )
    async def ping(self, inter):
        await inter.response.send_message(
            'Latency Returned {}ms'.format(round(self.bot.latency * 1000)), ephemeral=True
        )


    @commands.slash_command(
        name = 'server',
        description = "Returns Info About Guild"
    )
    @commands.has_any_role(
        "Owner", "Gawther", "Head Administrator", "Head Developer",
        "Head Designer", "Head Support", "Administrator", "Moderator",
        "Support Staff", "Community Helper", "DND_DM", "DND PL", "Developers",
        "Designers", "Nitro Member", "Programming", "Gaming", "Member"
    )
    async def server(self, inter):
        guild = self.bot.get_guild(guild_id)
        created_at_corrected = guild.created_at.__format__("%m/%d/%Y - %H:%M:%S")

        embed = disnake.Embed(
            color=disnake.Colour.random(),
            title="{} Server Info".format(guild.name),
            description = "Below you can find information about {}".format(guild.name)
        ).add_field(
            name="Creation Information",
            value="Created At: {}\nHead Robot: {}".format(created_at_corrected, self.bot.user.name),
            inline=False
        ).set_thumbnail(
            url = self.bot.get_guild(guild_id).icon
        ).set_footer(
            text = "To Apply For Any Of The _Applications Open_ Positions, Please [Click Here]()"
        )

        list_to_ignore = [
            "@everyone",
            "Muted",
            "Banned",
            "Kicked",
            "Member",
            "Gaming",
            "Programming",
            "Designers",
            "Developers",
            "DND PL",
            "DND_DM"
        ]

        # iterate through guilds roles
        for role in guild.roles[::-1]:
            # check for specific role names to skip
            if role.managed or role.name in list_to_ignore:
                pass
            # build member list
            else:
                # create blank list
                all_mems = ""

                # iterate through members in list
                for member in role.members:
                    # if member exists
                    if member:
                        # create a new name with a comma attached
                        name = member.name+', '
                        # add new name to blank list
                        all_mems += name
                    # otherwise, if member isn't found, pass
                    else:
                        pass

                # check to see if our newly created list (which is a sentence) has anything in it
                if all_mems == "":
                    # if so, add embed showing applications open
                    embed.add_field(
                        name=role.name,
                        value="Applications Open",
                        inline=False
                    )
                else:
                    # if not, add embed showing list of members in role
                    embed.add_field(
                        name=role.name,
                        value=all_mems,
                        inline=False
                    )

        await inter.response.send_message(
            embed=embed, ephemeral=True
        )


    @commands.slash_command(
        name="whois",
        description="Returns a profile on the user."
    )
    @commands.has_any_role(
        "Owner", "Gawther", "Head Administrator", "Head Developer",
        "Head Designer", "Head Support", "Administrator", "Moderator",
        "Support Staff", "Community Helper", "DND_DM", "DND PL", "Developers",
        "Designers", "Nitro Member", "Programming", "Gaming", "Member"
    )
    async def whois(self, inter, member:disnake.Member=None):
        if member is None:
            member = inter.author

        embed = disnake.Embed(
            color = disnake.Colour.random(),
            timestamp = inter.created_at,
            title = "Who Is {}?".format(member.name),
            description = "Below Is {}'s Profile Information".format(member.name)
        ).set_thumbnail(
            url = member.avatar
        )

        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            srch = 'SELECT * FROM members WHERE id=?'
            val = (member.id,)

            user_items = cur.execute(srch, val).fetchall()[0]

            embed.add_field(
                name="General Information",
                value=f"""Member ID: {member.id}
                            Member Name: {member.name}
                            Member Nick: {member.nick}
                            Member Age: {user_items[-2]}
                            Member Birthday: {user_items[-1]}""",
                inline=False
            ).add_field(
                name="Account Information",
                value=f"""Current Experience: {user_items[1]}
                        Current Level: {user_items[2]}""",
                inline=False
            ).add_field(
                name="Favorite Things",
                value=f"""Color: {user_items[3]}
                        Animal: {user_items[4]}
                        Food: {user_items[5]}
                        Educational Subject: {user_items[6]}
                        Music Artist: {user_items[7]}
                        Art Artist: {user_items[8]}
                        Season: {user_items[9]}
                        Holiday: {user_items[10]}""",
                inline=False
            )

        await inter.response.send_message(embed=embed, ephemeral=True)



def setup(bot):
    bot.add_cog(TierSixCommands(bot))