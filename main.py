import bot_initialization
from bot_initialization import client
import project_manager
import json

import discord
from discord.ext import commands
import db_utils as db
from datetime import datetime, timedelta
import time
import sched

# ***************************************************************************
# ***************************************************************************
# *********************** General Events & Commands *************************
# ***************************************************************************


@client.event
async def on_ready():
    db.connect()
    print('READY')

#######################################################################

#db.initializeDB()
#db.insertResult("60f19dd5597abc3621cc7aed", None, None)
client.run(json.load(open("bot_creds.json"))["bot"])
