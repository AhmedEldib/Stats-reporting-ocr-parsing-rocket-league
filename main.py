import bot_initialization
from bot_initialization import client
import project_manager
import json

#***************************************************************************
#***************************************************************************
#*********************** General Events & Commands *************************
#***************************************************************************
@client.command()
async def hi(ctx):
    await ctx.send('ready')

client.run(json.load(open("bot_creds.json"))["bot"])