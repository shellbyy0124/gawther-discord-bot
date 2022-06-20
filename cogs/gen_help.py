import disnake
import os
import sys
import json

from disnake.ext import commands
from disnake.ext.commands import Cog
from Paginator import CreatePaginator

if not os.path.isfile('config.json'):
    sys.exit("'config.json' Not Found!")
else:
    with open('./config.json','r',encoding='utf-8-sig') as f:
        data = json.load(f)

guild_id = data["bot_info"]["guild_id"]


class GeneralHelpCommands(Cog):
    def __init__(self,bot):
        self.bot = bot


    @commands.slash_command(
        name="gen_help",
        description="Returns The General Help Menu"
    )
    @commands.has_any_role(
        "Owner", "Gawther", "Head Administrator", "Head Developer",
        "Head Designer", "Head Support", "Administrator", "Moderator",
        "Support Staff", "Community Helper", "DND_DM", "DND PL", "Developers",
        "Designers", "Nitro Member", "Programming", "Gaming", "Member"
    )
    async def gen_help_menu(self,inter):
        all_embeds = []
        timeout = 0
        author_id = inter.author.id

        titles = [
            "/listrules",
            "/ping",
            "/server",
            "/whois <member>",
            "/appeal_ban <type>"
        ]

        descrip = [
            "Returns a Paginator Embed displaying all the rules for the website and discord alike.",
            "Returns the bots latency. If this number is extremely high, please contact support.",
            "Returns information about the discord server including who the owner is, and members of each staff role.",
            "Returns a solid embed displaying information entered using the CURRENTLY BEING BUILT /create_profile command.",
            "Can only be executed in the #how_to_appeal text channel located in the Support category. Allows a user to determine whether they want to appeal a mute, ban, or kick log."
        ]

        embed = disnake.Embed(
            color = disnake.Colour.random(),
            timestamp = inter.created_at,
            title = "{}'s General Help Menu".format(self.bot.get_guild(guild_id).name),
            description = "The Following Pages Will Show Available Commands and How To Use Them."
        ).set_thumbnail(
            url=self.bot.get_guild(guild_id).icon
        )

        all_embeds.append(embed)

        for i in range(len(titles)):
            embed_title = titles[i]
            embed_description = descrip[i]

            embed = disnake.Embed(
                color = disnake.Colour.random(),
                timestamp = inter.created_at,
                title = embed_title,
                description = embed_description
            ).set_thumbnail(
                url = self.bot.get_guild(guild_id).icon
            )

            all_embeds.append(embed)

        await inter.response.send_message(embed=all_embeds[0],view=CreatePaginator(all_embeds,author_id,timeout), ephemeral=True)


def setup(bot):
    bot.add_cog(GeneralHelpCommands(bot))