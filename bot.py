import json
import os
import sys
import disnake

from disnake.ext import commands
from createDb import create_db

"""remove before production"""
if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found!")
else:
    with open('./config.json','r',encoding='utf-8-sig') as f:
        data = json.load(f)

token = data["bot_info"]["token"]
cp = data["bot_info"]["cp"]

intents = disnake.Intents.all()

bot = commands.Bot(
    command_prefix=cp,
    intents=intents,
    guild_ids=[
        data["bot_info"]["guild_id"], #remove before production
    ],
    sync_commands_debug=True
)

@bot.event
async def on_ready():
    with open('./config.json','r',encoding="utf-8-sig") as f:
        data = json.load(f)
        
        for guild in bot.guilds:
            if guild.id == data["bot_info"]["guild_id"]:
                for channel in guild.text_channels:
                    if channel.id == data["bot_info"]["term_chan"]:
                        await channel.send('Gawther Is Online!')

for filename in os.listdir('./cogs'):
    if filename.endswith('py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(filename, 'loaded')

@bot.command()
@commands.is_owner()
async def update(ctx):
    async def start():
        os.system("python ./bot.py")
        await confirm()
    await ctx.send("Gawther will reset now")
    await start()

async def confirm(ctx):
    await ctx.send("Restart Complete")


if __name__ == '__main__':
    create_db()
    bot.run(token)