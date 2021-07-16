from bot_initialization import client
import functions
import re
from spreed_sheet import create_worksheet
import db_utils as db
from pymongo.errors import DuplicateKeyError
import sys

spreedsheet_link = []
spreedsheet_link.append("ur Spreadsheet link here with edit permission")

# *********************** rocket stats *************************
@client.command(name='a')
async def a(ctx, *args):

    try:
        game_number = args[0]
        link = args[1]

    except:
        await ctx.channel.send("Command missing the link or the Game ID")
        return

    # try:
    #     img = functions.download_image(message.attachments[0].url)
    #     team_1, team_2 = functions.get_stats(img)
    #     await message.channel.send("TEAM 1 \n" + "``` " + str(team_1) + " ``` \n" + "TEAM 2 \n" + "``` " + str(team_2) + " ```")

    # except:

    try:
        img = functions.download_image(link)
        team_1, team_2 = functions.get_stats(
            img, game_number, spreedsheet_link[0])
        await ctx.channel.send("TEAM 1 \n" + "``` " + str(team_1) + " ``` \n" + "TEAM 2 \n" + "``` " + str(team_2) + " ```" + "\n The stats can be found here : " + spreedsheet_link[0])

    except:
        await ctx.channel.send('Invalid Image')
        return

#######################################################################


@client.command(name='r')
async def r(ctx, *args):

    try:
        link = args[0]

    except:
        await ctx.channel.send("Command missing the link or the Game ID")
        return

    # try:
    #     replay = functions.download_replay(message.attachments[0].url)
    #     blue, orange = functions.parse_replay(replay)
    #     await ctx.channel.send("Blue Team \n" + "``` " + blue + " ``` \n" + "Orange Team \n" + "``` " + orange + " ```")

    # except:
    try:
        replay = functions.download_replay(link)
        blue, orange = functions.parse_replay(replay)
        await ctx.channel.send("Blue Team \n" + "``` " + blue + " ``` \n" + "Orange Team \n" + "``` " + orange + " ```")

    except:
        print('not a valid replay')
        return

#######################################################################


@client.command(name='s')
async def s(ctx, *args):
    try:
        if len(args) == 0:
            raise("No Link")

    except:
        await ctx.channel.send("Pls insert a Spreadsheet link")
        return

    try:
        create_worksheet(args[0])
        spreedsheet_link[0] = args[0]

        await ctx.channel.send("Switched to the new SpreadSheet")

    except:
        await ctx.author.send("Couldn't Open Spreadsheet. Try giving access to this mail as an editor: \n ```ur bot api link``` ")


#######################################################################
@client.command(name='ap')
async def ap(ctx, *args):
    player = ''
    try:
        if len(args) == 4:
            player = ctx.message.author.id
            db.insertNewPlayer(ctx.message.author.id,
                               args[0], args[1], args[2], args[3])
            await ctx.channel.send(ctx.message.author.mention + " is now a player")
        elif len(args) == 5:
            player = re.sub(r'[<@!>]', '', args[0])
            db.insertNewPlayer(player,
                               args[1], args[2], args[3], args[4])
            await ctx.channel.send("<@!"+str(player)+">"+" is now a player")
    except DuplicateKeyError:
        await ctx.channel.send("Player "+ctx.message.author.mention+" already registered")
    except:
        print(sys.exc_info())


#######################################################################
@client.command(name='at')
async def at(ctx, *args):
    try:
        db.insertTeam(args[0], re.sub(r'[<@!>]', '', args[1]), re.sub(
            r'[<@!>]', '', args[2]), re.sub(r'[<@!>]', '', args[3]))
        await ctx.channel.send(args[0]+" is now a team")
    except DuplicateKeyError:
        await ctx.channel.send("Team name is already taken or members in this team already have a team")
    except:
        print(sys.exc_info())

#######################################################################
@client.command(name='am')
async def am(ctx, *args):
    db.insertMatch(args[2], args[3], args[0], args[1])

#######################################################################
