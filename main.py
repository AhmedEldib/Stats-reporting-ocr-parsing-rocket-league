import bot_initialization
from bot_initialization import client
import project_manager

#***************************************************************************
#***************************************************************************
#*********************** General Events & Commands *************************
#***************************************************************************
@client.command()
async def hi(ctx):
    await ctx.send('Hello there!')

client.run('Bot Token Here')