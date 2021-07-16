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

#***************************************************************************
#***************************************************************************
#*********************** General Events & Commands *************************
#***************************************************************************

@client.event
async def on_ready():
    db.connect()
    print('READY')

#######################################################################

# async def time_check():
#     await client.wait_until_ready()
#     while not client.is_closed():
#         channel = client.get_channel(726075186474123306)
#         f = '%H:%M'

#         alarm_time = '16:45'

#         now = datetime.strftime(datetime.now(), f)
#         # get the difference between the alarm time and now
#         diff = (datetime.strptime(alarm_time, f) -
#                 datetime.strptime(now, f)).total_seconds()

#         # create a scheduler
#         s = sched.scheduler(time.perf_counter, time.sleep)
#         # enter the command and arguments into the scheduler
#         args = (await channel.send(diff), )
#         s.enter(5, 1, client.loop.create_task, args)
#         s.run()  # run the scheduler, will block the event loop


#client.loop.create_task(time_check())
#db.initializeDB()
client.run(json.load(open("bot_creds.json"))["bot"])
