import disnake
import sys
import os
import json

import sqlite3 as sql

from disnake.ext import commands
from disnake.ext.commands import Cog
from Paginator import CreatePaginator

if not os.path.isfile('config.json'):
    sys.exit("'config.json' Not Found!")
else:
    with open('./config.json', 'r', encoding='utf-8-sig') as f:
        data = json.load(f)


guild_id = data["bot_info"]["guild_id"]


class TierSevenCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    # muted, banned, kicked commands => only appeal commands

    @commands.slash_command(
        name="appeal_ban",
        description="/appeal_ban <ban/kick/mute>"
    )
    @commands.has_any_role(
        "Banned", "Kicked", "Muted", "Head Developer"
    )
    async def appeal_ban(self, inter, type: str):
        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            if inter.channel_id == 987495649358520330:
                if type.lower() == "mute":
                    srch = 'SELECT * FROM mute_logs WHERE id=?'
                    val = (inter.author.id,)

                    all_logs = cur.execute(srch, val).fetchall()

                    if all_logs:
                        embed = disnake.Embed(
                            color=disnake.Colour.random(),
                            timestamp=inter.created_at,
                            title="{}'s Appeal Moderator".format(
                                self.bot.get_guild(guild_id).name),
                            description="Below Are All Your Logs. Enter The Corresponding Number You Want To Appeal. ONLY ONE!"
                        ).set_thumbnail(
                            url=self.bot.get_guild(guild_id).icon
                        ).set_footer(
                            text="WARNING: Do Not Spam! We Will Be With You As Soon As Possible!"
                        )

                        count = 1
                        emb_name = "embed"+str(count)

                        all_embs = [embed]

                        for item in all_logs:
                            emb_name = disnake.Embed(
                                title="{}".format(item[1]),
                                description=f"""User ID: {item[0]}
                                        User Name: {inter.author.name}
                                        Date Initiated: {item[3]}
                                        Staff Member: {item[2]}
                                        Start Time: {item[3]}
                                        End Time: {item[4]}"""
                            ).add_field(
                                name="Reason",
                                value=item[-1],
                                inline=False
                            ).set_thumbnail(
                                url=self.bot.get_guild(guild_id).icon
                            ).set_footer(
                                text="WARNING: Do Not Spam! We Will Be With You As Soon As Possible!"
                            )

                            all_embs.append(emb_name)
                            count += 1

                        timeout = 0
                        author_id = inter.author.id

                        await inter.response.send_message(embed=all_embs[0],view=CreatePaginator(all_embs, author_id, timeout),ephemeral=True)
                    else:
                        return await inter.response.send_message("You Have No Mutes To Appeal, {}".format(inter.author.mention), delete_after=30)
                elif type.lower() == "kick":
                    srch = 'SELECT * FROM kick_logs WHERE id=?'
                    val = (inter.author.id,)

                    all_logs = cur.execute(srch, val).fetchall()

                    if all_logs:
                        embed = disnake.Embed(
                            color=disnake.Colour.random(),
                            timestamp=inter.created_at,
                            title="{}'s Appeal Moderator".format(
                                self.bot.get_guild(guild_id).name),
                            description="Below Are All Your Logs. Enter The Corresponding Number You Want To Appeal. ONLY ONE!"
                        ).set_thumbnail(
                            url=self.bot.get_guild(guild_id).icon
                        ).set_footer(
                            text="WARNING: Do Not Spam! We Will Be With You As Soon As Possible!"
                        )

                        count = 1
                        emb_name = "embed"+str(count)

                        all_embs = [embed]

                        for item in all_logs[::-1]:
                            emb_name = disnake.Embed(
                                title="{}".format(item[1]),
                                description=f"""User ID: {item[0]}
                                        User Name: {inter.author.name}
                                        Date Initiated: {item[3]}
                                        Staff Member: {item[2]}
                                        Start Time: {item[3]}
                                        End Time: {item[4]}"""
                            ).add_field(
                                name="Reason",
                                value=item[-1],
                                inline=False
                            ).set_thumbnail(
                                url=self.bot.get_guild(guild_id).icon
                            ).set_footer(
                                text="WARNING: Do Not Spam! We Will Be With You As Soon As Possible!"
                            )

                            all_embs.append(emb_name)
                            count += 1

                        timeout = 0
                        author_id = inter.author.id

                        await inter.response.send_message(embed=all_embs[0],view=CreatePaginator(all_embs, author_id, timeout),ephemeral=True)
                    else:
                        return await inter.response.send_message("You Have No Kicks To Appeal, {}".format(inter.author.mention), delete_after=30)
                elif type.lower() == "ban":
                    srch = 'SELECT * FROM ban_logs WHERE id=?'
                    val = (inter.author.id,)

                    all_logs = cur.execute(srch, val).fetchall()

                    if all_logs:
                        embed = disnake.Embed(
                            color=disnake.Colour.random(),
                            timestamp=inter.created_at,
                            title="{}'s Appeal Moderator".format(
                                self.bot.get_guild(guild_id).name),
                            description="Below Are All Your Logs. Enter The Corresponding Number You Want To Appeal. ONLY ONE!"
                        ).set_thumbnail(
                            url=self.bot.get_guild(guild_id).icon
                        ).set_footer(
                            text="WARNING: Do Not Spam! We Will Be With You As Soon As Possible!"
                        )

                        count = 1
                        emb_name = "embed"+str(count)

                        all_embs = [embed]

                        for item in all_logs[::-1]:
                            emb_name = disnake.Embed(
                                title="{}".format(item[1]),
                                description=f"""User ID: {item[0]}
                                        User Name: {inter.author.name}
                                        Date Initiated: {item[3]}
                                        Staff Member: {item[2]}
                                        Start Time: {item[3]}
                                        End Time: {item[4]}"""
                            ).add_field(
                                name="Reason",
                                value=item[-1],
                                inline=False
                            ).set_thumbnail(
                                url=self.bot.get_guild(guild_id).icon
                            ).set_footer(
                                text="WARNING: Do Not Spam! We Will Be With You As Soon As Possible!"
                            )

                            all_embs.append(emb_name)
                            count += 1

                        timeout = 0
                        author_id = inter.author.id

                        await inter.response.send_message(embed=all_embs[0],view=CreatePaginator(all_embs, author_id, timeout),ephemeral=True)
                    else:
                        return await inter.response.send_message("You Have No Bans To Appeal, {}".format(inter.author.mention), delete_after=30)
                else:
                    return await inter.response.send_message("Incorrect Type. Enter ban/kick/mute as your type choice for the command, {}".format(inter.author.mention), delete_after=30)
            else:
                return await inter.response.send_message("You Are Not In The {} Channel!".format(
                    self.bot.get_channel(987495649358520330).mention
                ), delete_after=30)



def setup(bot):
    bot.add_cog(TierSevenCommands(bot))
