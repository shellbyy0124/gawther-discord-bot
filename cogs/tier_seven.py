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
                description="Appeal a Mute Log"
            ),
            disnake.SelectOption(
                label="Kick",
                description="Appeal A Kick Log"
            ),
            disnake.SelectOption(
                label="Ban",
                description="Appeal A Ban Log"
            )
        ]

        super().__init__(
            placeholder="Select One",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self,inter):
        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            srch = f'SELECT {inter.values[0].lower()}_id FROM {inter.values[0].lower()}_logs WHERE id=?'
            val = (inter.author.id,)

            results = cur.execute(srch, val).fetchone()

            if results:
                print(results)
                log_channel = disnake.utils.get(inter.guild.text_channels, name="appeals")
                await log_channel.send(f":rotating_light:Incoming Appeal Request:rotating_light:\n{inter.author.name} is wanting to appeal a {inter.values[0]} log. Please pull them into a channel at your earliest convenience and use the `/mem_prof_staff <name/id>` command to see all relavent information.")
                await inter.response.edit_message("Your Request Has Been Sent. Please Be Patient And We Will Be With You As Soon As Possible.",view=None)
            else:
                return await inter.response.edit_message(f"You Do Not Have Any {inter.values[0]} Logs, {inter.author.mention}",view=None)


class AppealFunctions(Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.slash_command(name="appeal_ban",description="Appeal A Log On Your Record")
    @commands.has_any_role("Head Developer","Banned","Kicked","Muted")
    async def appeal_ban(self,inter):
        if inter.channel.name == "how_to_appeal":
            view = BotView(self.bot)
            await inter.response.send_message("Please Select An Item Below", view=view)
        else:
            return await inter.response.send_message(
                "You Are Not In The {} Channel!".format(
                    self.bot.get_channel(987495649358520330).mention
            ), delete_after=30)


def setup(bot):
    bot.add_cog(AppealFunctions(bot))