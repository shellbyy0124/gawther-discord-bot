import disnake
import sqlite3 as sql

from disnake.ext import commands
from disnake.ext.commands import Cog
from Paginator import CreatePaginator


class BotView(disnake.ui.View):
    def __init__(self,bot:commands.Bot):
        super().__init__()
        self.bot = bot
        self.add_item(Dropdown())


class DropdownView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())

    
class Dropdown(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(
                label="Mute",
                description="Select If User Has Selected A Mute Appeal"
            ),
            disnake.SelectOption(
                label="Kick",
                description="Select If User Has Selected A Kick Appeal"
            ),
            disnake.SelectOption(
                label="Ban",
                description="Select If User Has Selected A Ban Appeal"
            )
        ]

        super().__init__(
            placeholder="Select One",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self,inter):
        choice = inter.values[0]
        msg = await inter.channel.send("Enter Member's ID",view=None)
        iden = await inter.bot.wait_for('message')
        await msg.delete()
        await iden.delete()
        all_embeds = []
        titles = ["ID","Exp","Level","Warnings","Mutes","Kicks","Bans"]
        titles2 = ["ID","Log ID","Staff Member","Start Time","End Time","Reason"]

        if all(i.isnumeric() for i in iden.content):
            with sql.connect('main.db') as mdb:
                cur = mdb.cursor()

                srch = 'SELECT id,exp,level,warnings,mutes,bans,kicks FROM members WHERE Id=?'
                val = (iden.content,)

                srch2 = f'SELECT * FROM {choice.lower()}_logs WHERE id=?'
                val2 = (iden.content,)

                all_mem_info = cur.execute(srch, val).fetchall()
                all_log_info = cur.execute(srch2, val2).fetchall()

                embed = disnake.Embed(
                    color = disnake.Colour.random(),
                    timestamp = inter.created_at,
                    title = "General information",
                    description = "Account Information"
                )

                for title in titles:
                    embed.add_field(
                        name="\u200b",
                        value=f"{title}: {all_mem_info[0][titles.index(title)]}",
                        inline=False
                    )

                all_embeds.append(embed)

                if all_log_info:
                    embed2 = disnake.Embed(
                        color = disnake.Colour.random(),
                        timestamp = inter.created_at,
                        title = "Log Information",
                        description = f"Members {choice} Logs"
                    )

                    for title2 in titles2:
                        embed2.add_field(
                            name="\u200b",
                            value=f"{title2}: {all_log_info[0][titles2.index(title2)]}",
                            inline=False
                        )

                    all_embeds.append(embed2)
                    await inter.response.edit_message(embed=all_embeds[0],view=CreatePaginator(all_embeds[::-1],inter.author.id,timeout)) 
                else:
                    return await inter.response.edit_message("User Has No Log Info",view=None)
              

        else:
            return await inter.response.edit_message("User's ID Must Be An Integer (Whole Number)",view=None)


class TierOneCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    # owner and/or owner and head position commands

    @commands.slash_command(name="mem_prof_staff",description="Shows All Of The Designated Users Information That Is Stored In The Database.")
    @commands.has_any_role("Owner","Head Administrator","Head Support","Head Designer","Head Developer")
    async def show_profile(self,inter):
        if inter.channel.name == "appeal_discussion":
            view = BotView(self.bot)
            await inter.response.send_message("Select Type Of Member Appeal",view=view)
        else:
            ping = disnake.utils.get(inter.guild.text_channels, name="appeal_discussion")
            await inter.response.defer("Invalid Channel. {}".format(ping.mention), delete_after=30)


def setup(bot):
    bot.add_cog(TierOneCommands(bot))