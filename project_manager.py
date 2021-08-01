from bot_initialization import client
import functions
import re
from spreed_sheet import create_worksheet
import db_utils as db
from pymongo.errors import DuplicateKeyError
import sys
import asyncio


# spreedsheet_link = []
# spreedsheet_link.append("ur Spreadsheet link here with edit permission")

# *********************** rocket stats OCR*************************


# @client.command(name='a')
# async def a(ctx, *args):

#     try:
#         game_number = args[0]
#         link = args[1]

#     except:
#         await ctx.channel.send("Command missing the link or the Game ID")
#         return

#     # try:
#     #     img = functions.download_image(message.attachments[0].url)
#     #     team_1, team_2 = functions.get_stats(img)
#     #     await message.channel.send("TEAM 1 \n" + "``` " + str(team_1) + " ``` \n" + "TEAM 2 \n" + "``` " + str(team_2) + " ```")

#     # except:

#     try:
#         img = functions.download_image(link)
#         team_1, team_2 = functions.get_stats(
#             img, game_number, spreedsheet_link[0])
#         await ctx.channel.send("TEAM 1 \n" + "``` " + str(team_1) + " ``` \n" + "TEAM 2 \n" + "``` " + str(team_2) + " ```" + "\n The stats can be found here : " + spreedsheet_link[0])

#     except:
#         await ctx.channel.send('Invalid Image')
#         return

#######################################################################


@client.command(name='replay')
async def parse_replay(ctx, *args):

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
        await ctx.channel.send("Blue Team \n" + "``` " + blue.to_string(index=False) + " ``` \n" + "Orange Team \n"
                               + "``` " + orange.to_string(index=False) + " ```")

    except:
        print('not a valid replay')
        return

#######################################################################


# @client.command(name='s')
# async def s(ctx, *args):
#     try:
#         if len(args) == 0:
#             raise("No Link")

#     except:
#         await ctx.channel.send("Pls insert a Spreadsheet link")
#         return

#     try:
#         create_worksheet(args[0])
#         spreedsheet_link[0] = args[0]

#         await ctx.channel.send("Switched to the new SpreadSheet")

#     except:
#         await ctx.author.send("Couldn't Open Spreadsheet. Try giving access to this mail as an editor: \n ```ur bot api link``` ")


#######################################################################
@client.command(name='player')
async def add_player(ctx, *args):
    player = ''
    try:
        if len(args) == 5:
            player = ctx.message.author.id
            db.insertNewPlayer(ctx.message.author.id,
                               args[0], args[1], args[2], args[3], args[4])
            await ctx.channel.send(ctx.message.author.mention + " is now a player")
        elif len(args) == 6:
            player = re.sub(r'[<@!>]', '', args[0])
            db.insertNewPlayer(player,
                               args[1], args[2], args[3], args[4], args[5])
            await ctx.channel.send("<@!" + str(player) + ">" + " is now a player")
    except DuplicateKeyError:
        await ctx.channel.send("Player " + ctx.message.author.mention + " already registered")
    except:
        print(sys.exc_info())


#######################################################################
@client.command(name='team')
async def add_team(ctx, *args):
    try:
        db.insertTeam(args[0], re.sub(r'[<@!>]', '', args[1]), re.sub(
            r'[<@!>]', '', args[2]), re.sub(r'[<@!>]', '', args[3]), re.sub(r'[<@!>]', '', args[4]) if len(args) == 5 else None)
        await ctx.channel.send(args[0]+" is now a team")
    except DuplicateKeyError:
        await ctx.channel.send("Team name is already taken or members in this team already have a team")
    except:
        print(sys.exc_info())

#######################################################################


@client.command(name='match')
async def add_match(ctx, *args):
    if len(args) == 10:
        team1 = {'name': args[0], 'who': [args[1], args[2], args[3]]}
        team2 = {'name': args[4], 'who': [args[5], args[6], args[7]]}
        matchID = db.insertMatch(args[8], args[9], team1, team2)
    else:
        team1 = {'name': args[0], 'who': ['captain', 'player2', 'player3']}
        team2 = {'name': args[1], 'who': ['captain', 'player2', 'player3']}
        matchID = db.insertMatch(args[2], args[3], team1, team2)
    await ctx.channel.send("Match is created with ID:"+str(matchID))

#######################################################################
# @client.command(name='pID')
# async def pID(ctx, *args):
#     for id in args:
#         print(id)
#######################################################################
@client.command(name='result')
async def get_result(ctx, *args):
    matchID = args[0]
    replay = functions.download_replay(args[1])
    blue, orange = functions.parse_replay(replay)
    db.insertResult(matchID, blue, orange)

#######################################################################
@client.command(name='stats')
async def stats(ctx, *args):
    players, teams, matches = db.exctractDataFrames()
    players.to_csv('players.csv')
    teams.to_csv('teams.csv')
    matches.to_csv('matches.csv')
#######################################################################
@client.command(name='pop')
async def stats(ctx, *args):
    db.removeLastReplay(args[0])
#######################################################################
@client.command(name='commit')
async def stats(ctx, *args):
    db.commitSeries(args[0])
#######################################################################
@client.command(name='uncommit')
async def stats(ctx, *args):
    db.uncommitSeries(args[0])
#######################################################################
@client.command(name='view')
async def stats(ctx, *args):
    date, df = db.getSeries(args[0])
    teams = list(df['Team'].unique())
    await ctx.channel.send('Series: '+str(teams[0]) + ' vs ' + str(teams[1]) + ' on: ' + str(date.day) + '/' + str(date.month) + ' ' + str(date.hour) + ':' + str(date.minute))
    for match in df['Game number'].unique():
        await ctx.channel.send('Match #'+str(match))
        await ctx.channel.send("```" + df[df['Game number'] == match].drop('Game number', axis=1).set_index('Player').to_string() + "```")
#######################################################################
