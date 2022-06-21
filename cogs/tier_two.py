import disnake
import json
import asyncio
import sqlite3 as sql

from disnake.ext import commands
from disnake.ext.commands import Cog
from datetime import datetime, timedelta


class TierTwoCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    # H. Admin, H. Support, H. Designer, H. Developer commands

    @commands.slash_command(name="ban_member",description="Ban A Member")
    @commands.has_any_role("Owner", "Gawther", "Head Administrator", "Head Support", "Head Designer", "Head Developer")
    async def mem_ban(self, inter, member: disnake.Member, time: int, *, reason: str):
        embed = disnake.Embed(
            color=disnake.Colour.red(),
            timestamp=inter.created_at,
            title="{}'s Moderation System".format(self.bot.user.name),
            description="Member: {}\nStaff Member: {}\nType: Banned\nTime To Serve: {}".format(
                member.name, inter.author.name, str(time)
            )
        ).add_field(
            name="Reason",
            value=reason,
            inline=False
        ).set_footer(
            text="To Appeal This Decision, Please Use The '/appealban' command."
        ).set_thumbnail(url=self.bot.user.avatar)

        member_current_roles = member.roles
        ban_role = disnake.utils.get(inter.guild.roles, name="Banned")
        log_channel = disnake.utils.get(inter.guild.text_channels, name="ban_logs")

        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            srch = 'SELECT bans FROM members WHERE id=?'
            val = (member.id,)

            current_count = cur.execute(srch, val).fetchone()

            if current_count:
                new_count = current_count[0] + 1

                srch2 = 'UPDATE members SET bans=? WHERE id=?'
                val2 = (new_count, member.id,)

                cur.execute(srch2, val2)

                total_logs = cur.execute('SELECT * FROM ban_logs').fetchall()

                ban_id = len(total_logs) + 1

                start = datetime.now()
                end = datetime.now() + timedelta(seconds=time)

                srch3 = 'INSERT INTO ban_logs(id,ban_id,staff,start_time,end_time,reason) VALUES (?,?,?,?,?,?)'
                val3 = (member.id, ban_id, inter.author.id, start, end, reason)

                cur.execute(srch3, val3)

                for channel in self.bot.get_guild(guild_id).voice_channels:
                    for mem in channel.members:
                        if mem.id == member.id:
                            await member.move_to(None)

                await member.send(embed=embed)
                await log_channel.send(embed=embed)
                await inter.response.send_message("Successfully Banned {}".format(member.name), ephemeral=True)
                await member.edit(roles=[ban_role])

                while time > 0:
                    await asyncio.sleep(1)
                    time -= 1
                else:
                    await member.edit(roles=member_current_roles)

                await member.send("Your Ban Has Been Lifted, {}".format(member.mention))
            else:
                new_count = 1

                srch2 = 'UPDATE members SET bans=? WHERE id=?'
                val2 = (new_count, member.id,)

                cur.execute(srch2, val2)

                total_logs = cur.execute('SELECT * FROM ban_logs').fetchall()

                ban_id = len(total_logs) + 1

                start = datetime.now()
                end = datetime.now() + timedelta(seconds=time)

                srch3 = 'INSERT INTO ban_logs(id,ban_id,staff,start_time,end_time,reason) VALUES (?,?,?,?,?,?)'
                val3 = (member.id, ban_id, inter.author.id, start, end, reason)

                cur.execute(srch3, val3)

                for channel in self.bot.get_guild(guild_id).voice_channels:
                    for mem in channel.members:
                        if mem.id == member.id:
                            await member.move_to(None)

                await member.send(embed=embed)
                await log_channel.send(embed=embed)
                await inter.response.send_message("Successfully Banned {}".format(member.name), ephemeral=True)
                await member.edit(roles=[ban_role])

                while time > 0:
                    await asyncio.sleep(1)
                    time -= 1
                else:
                    await member.edit(roles=member_current_roles)

                await member.send("Your Ban Has Been Lifted, {}".format(member.mention))

    @commands.slash_command(name="update_database",description="Updates Database To Insert Non-Existent Members")
    @commands.has_any_role("Owner","Head Developer")
    async def update_mems(self, inter):
        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            for member in inter.guild.members:
                if not member.bot:
                    srch = 'INSERT INTO members(id,\
                        exp,level,color,animal,food,edu_subj,\
                            artist_music,artist_art,season,holiday,\
                                warnings,mutes,bans,kicks,age,dob) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
                    val = (member.id, 0, 0, "empty", "empty", "empty", "empty",
                           "empty", "empty", "empty", "empty", 0, 0, 0, 0, 0, "empty")
                    cur.execute(srch, val)

        await inter.response.send_message("Finished Updating Members & Database", ephemeral=True)

    @commands.slash_command(name="purge",description="Deletes _N_ Messages From The Channel Executed In")
    @commands.has_any_role("Owner", "Head Developer", "Head Administrator", "Head Designer", "Head Support")
    async def purge_message(self, inter, num: int, *, reason: str):
        if num > 25:
            return await inter.response.send_message("Do Not Purge More Than 25 Messages At A Time, {}".format(inter.author.mention), ephemeral=True)
        else:
            await inter.response.send_message(f"Purging {num} Message", ephemeral=True)
            await inter.channel.purge(limit=num)

            embed = disnake.Embed(
                color=disnake.Colour.random(),
                timestamp=inter.created_at,
                title="{}'s Purge Messages Command".format(inter.guild.name),
                description=f"User: {inter.author.name}\nAction: Purged\nWhere: {inter.channel.name}\nNumber Of Messages: {num}\nWhy: {reason}"
            ).set_thumbnail(url=self.bot.user.avatar)

            message = await inter.channel.history(limit=None).flatten()
            await inter.edit_original_message(f"Purging Of {num}/{len(message)} Messages Complete")
            log_channel = disnake.utils.get(inter.guild.text_channels, name="message_deletes")
            await log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(TierTwoCommands(bot))
