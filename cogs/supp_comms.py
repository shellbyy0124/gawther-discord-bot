import disnake 
import os
import sys
import json

from disnake.ext import commands
from disnake.ext.commands import Cog

if not os.path.isfile('config.json'):
    sys.exit("'config.json' Not Found!")
else:
    with open('./config.json','r',encoding='utf-8-sig') as f:
        data = json.load(f)

guild_id = data["bot_info"]["guild_id"]


"""
THIS PAGE IS LAID OUT IN THE FOLLOWING FORMAT

FIRST VIEW = BOTVIEW
SECOND VIEW = DISCORDSUPPORTVIEW -> ALL SUB VIEWS OF DISCORDSUPPORTVIEW WILL BE NAMED AS THE NUMBER AND VIEW
SECOND_ALPHA = WEBSITESUPPORTVIEW -> ALL SUB VIEWS OF WEBSITESUPPORTIVEW WILL BE NAMED AS THE NUMBER_ALPHA AND VIEW

LOOK FOR MULTI-LINE COMMENTS THROUGHOUT THIS SCRIPT TO FIND WHERE EACH VIEW STARTS AND STOPS AND WHAT VIEW IT BELONGS TO
"""

"""FIRST VIEW IS THE BOT VIEW."""
class BotView(disnake.ui.View):
    def __init__(self, bot:commands.Bot):
        super().__init__()
        self.bot = bot
        self.add_item(Dropdown())

"""BELONGS TO BOTVIEW"""
class DropdownView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())

"""BELONGS TO BOTVIEW"""
class Dropdown(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label = "Discord Support",description = "Follow On-Screen Prompts For Assistance Within The Discord Platform"),
            disnake.SelectOption(label = "Website Support",description = "Follow On-Screen Prompts For Assistance Within The Website Platform")
        ]

        super().__init__(
            placeholder="Select One",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self,inter):
        for value in inter.values:
            if value == "Discord Support":
                view = DiscordSupportView()
                await inter.response.edit_message("Please Select A Sub-Category Below ",view=view)
            elif value == "Website Support":
                view = WebsiteSupportView()
                await inter.response.edit_message("Please Select A Sub-Category Below",view=view)
            else:
                await inter.response.edit_message("Invalid Category. Report To Staff")

"""SECOND VIEW IS THE DISCORD SUPPORT VIEW."""
class DiscordSupportView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown2())

"""BELONGS TO DISCORDSUPPORTVIEW"""
class Dropdown2(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label = "Roles", description="Get Support With Your Current Role(s)"),
            disnake.SelectOption(label = "Voice", description="Get Support With Voice Channels"),
            disnake.SelectOption(label = "Text", description="Get Support With Text Channels"),
            disnake.SelectOption(label = "Categories", description="Get Support With A Category")
        ]

        super().__init__(
            placeholder="Select One",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self,inter):
        value = inter.values[0]

        embed = disnake.Embed(
            color = disnake.Colour.random(),
            timestamp = inter.created_at,
            title = "The Channel Now Belongs To {}. I have Gotten Them Started For You <3".format(inter.author.name),
            description = """Member ID: {}
                             Member Name: {}
                             Member Nick: {}
                             Category: Discord Support
                             Sub-Category: {}""".format(
                                 inter.author.id,
                                 inter.author.name,
                                 inter.author.nick,
                                 value
                             )
        ).add_field(
            name = "What Do I Do Now?",
            value = """Please enter as much information as you can for our support 
                       team to be able to help you with the best accuracy possible. 
                       Once you've submitted your information, PLEASE BE PATIENT. 
                       No one gets paid, and therefore will not be rushed. If it is an
                       emergency, call 9-1-1.""",
            inline = False
        ).set_thumbnail(url = inter.guild.icon)

        member = inter.author
        avai_cat = disnake.utils.get(inter.guild.categories, name="Available Support Channels")
        occu_cat = disnake.utils.get(inter.guild.categories, name="Occupied Support Channels")
        new_role_name = avai_cat.text_channels[0].name

        if new_role_name:
            new_role = []

            for role in inter.guild.roles:
                if role.name == new_role_name:
                    new_role.append(role)
                    break

            ping_role = disnake.utils.get(inter.guild.roles, name="clocked_in")
            await member.add_roles(new_role[0])

            for channel in inter.guild.text_channels:
                if channel.name == new_role_name:
                    await channel.edit(category=occu_cat)
                    a = "{}, Please enter in as many details as possible".format(inter.author.mention)
                    b = a + ' ' + "Whoemever is {} will be with you shortly :) <3".format(ping_role.mention)
                    await channel.send(b)
                    return await inter.response.edit_message("You've Been Mentioned In The Appropraite Channel")
        else:
            return await inter.response.edit_message("The Que System For Our Support Area Has Not Been Setup Yet. Please Wait For An Available Channel")
            """STARTING CODE FOR QUE SYSTEM"""
            # with open('./que.json','r',encoding='utf-8-sig') as g:
            #     rule_file = json.load(g)

            #     count = len(rule_file["que_list"].keys()) + 1

            #     rule_file["que_list"].append({
            #         str(count): {
            #             "mem_id": inter.author.id,
            #             "mem_name": inter.author.name,
            #             "mem_nick": inter.author.nick,
            #             "cat": "Discord Support",
            #             "subCat": value
            #         }
            #     })
            
            # with open('./que.json','w+',encoding='utf-8-sig') as new:
            #     data = json.dump(data, new, indent=4)

            # return await inter.response.edit_message(
            #     "There Are No Available Support Channels At\
            #         This Moment. Once A Channel Becomes Available\
            #             You Will Be Notified."
            # )

"""SECOND_ALPHA VIEW IS THE WEBSITE SUPPORT VIEW"""
class WebsiteSupportView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown3())

"""BELONGS TO WEBSITESUPPORTVIEW"""
class Dropdown3(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label="Forums", description="Get Support With Website Forum Actions"),
            disnake.SelectOption(label="Sign Up", description="Get Support With Signing Up For The Website"),
            disnake.SelectOption(label="Shop", description="Get Support With The Websites' Online Shop")
        ]

        super().__init__(
            placeholder="Select One",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self,inter):
        value = inter.values[0]

        if value == "Shop":
            return await inter.response.edit_message("The Online Shop For The Website Has Not Been Setup Yet.")
        elif value == "Sign Up":
            return await inter.response.edit_message("The Sign Up Process For The Website Has Not Been Setup Yet.")
        elif value == "Forums":
            return await inter.response.edit_message("The Forums For The Website Has Not Been Setup Yet.")
        else:
            return await inter.response.edit_message("Something went wrong. Contact Support")


class SupportFunctions(Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.slash_command(
        name="support",
        description="Get Support For Either Discord, Or The Website",
        guild_ids=[guild_id]
    )
    @commands.has_any_role(
        "Owner", "Gawther", "Head Administrator", "Head Developer",
        "Head Designer", "Head Support", "Administrator", "Moderator",
        "Support Staff", "Community Helper", "DND_DM", "DND PL", "Developers",
        "Designers", "Nitro Member", "Programming", "Gaming", "Member"
    )
    async def get_support(self,inter):
        view = BotView(self.bot)
        await inter.response.send_message("Please Select A Category Below", view=view, ephemeral=True)


def setup(bot):
    bot.add_cog(SupportFunctions(bot))
