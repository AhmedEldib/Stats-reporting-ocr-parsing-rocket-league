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

''' *********************** OCR & Spreedsheet Commands ************************* '''

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

''' *********************** Replays Parsing, Team, Players, Matches, Database commands ************************* '''

@client.command(name='replay')
async def parse_replay(ctx, *args):
    """Takes a replay link and returns the match properties after parsing it

    Command
    ----------
    ;replay <link>

    Parameters
    ----------
    *args : str
        The replay link 

    Raises
    ------
    Command missing the link or the Game ID
        If no link is in the command
    not a valid replay
        if the replay link couldn't be downloaded or not a replay or it is corrupted 
    """


    try:
        link = args[0]

    except:
        await ctx.channel.send("Command missing the link or the Game ID")
        return

    # using files instead of links (not to be used at the moment)
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
        await ctx.channel.send('not a valid replay')
        return

#######################################################################

@client.command(name='player')
async def add_player(ctx, *args):
    """Takes multiple arguments to create a new player document in the database

    Command
    ----------
    to add yourself :
        ;player <name> <mobile_number> <rank (tier)> <rocket_id> <tracker_link>
    to add another person :
        ;player <discord_id (mention)> <name> <mobile_number> <rank (tier)> <rocket_id> <tracker_link>

    Parameters
    ----------
    *args : array
        1: discord id of the player (optional to add someone else), 
        2: name of the player in game,
        3: mobile number (Egypt),
        4: tier of the player -> 1 = captain, 2 = second tier, 3 = third tier,
        5: in game rocket id
        6: rocket league tracker network profile link

    Raises
    ------
    There are still missing arguments.
        If the passed arguments are missing some enteries
    Player already registered
        if the discord id passed is already in the database
    """


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

        else:
            await ctx.channel.send('There are still missing arguments. \n format to add yourself should be: ' 
                                + ';player <name> <mobile_number> <rank (tier)> <rocket_id> <tracker_link>'
                                + ' \n format to add another person should be: '
                                + ';player <discord_id (mention)> <name> <mobile_number> <rank (tier)> <rocket_id> <tracker_link>')

    except DuplicateKeyError:
        await ctx.channel.send("Player " + ctx.message.author.mention + " already registered")
    except:
        print(sys.exc_info())

#######################################################################

@client.command(name='team')
async def add_team(ctx, *args):
    """Takes multiple arguments to create a new team along with its players who are already in the database

    Command
    ----------
    to create a team with only 1 player (captain) :
        ;team <team name> <captain mention> 
    to create a team with only multiple players :
        ;team <team name> <captain mention> <tier 2 player> <tier 3 player (optional)> <sub player (optional)>

    Parameters
    ----------
    *args : array
        1: team name, 
        2: captain discord id,
        3: second tier player discord id,
        4: third tier player discord id,
        5: sub player discord id

    Raises
    ------
    Team name is already taken or members in this team already have a team.
        If the passed team name is already taken or the players are in other teams
    """


    try:
        db.insertTeam(args[0], re.sub(r'[<@!>]', '', args[1]), re.sub(
            r'[<@!>]', '', args[2]) if len(args) == 3 else None, re.sub(r'[<@!>]', '', args[3]) if len(args) == 4 else None, re.sub(r'[<@!>]', '', args[4]) if len(args) == 5 else None)
        await ctx.channel.send(args[0]+" is now a team")
    except DuplicateKeyError:
        await ctx.channel.send("Team name is already taken or members in this team already have a team")
    except:
        print(sys.exc_info())

#######################################################################

@client.command(name='join')
async def join_team(ctx, *args):
    """Takes team name and new player with their role to join a team

    Command
    ----------
    to add a new player to the team :
        ;join <team name> <player mention> <role> 

    Parameters
    ----------
    *args : array
        1: team name, 
        2: player discord id,
        3: role -> captain = tier 1, player2 = tier 2, player3 = tier 3, sub = sub player

    Raises
    ------

    """


    try:
        db.joinTeam(args[0], re.sub(r'[<@!>]', '', args[1]), args[2])
        await ctx.channel.send(args[1]+" is now "+args[0]+' member')
    except:
        print(sys.exc_info())

#######################################################################

@client.command(name='kick')
async def kick_from_team(ctx, *args):
    """Takes team name and a player id to kick them from the team

    Command
    ----------
    to kick a player from the team :
        ;kick <team name> <player mention>

    Parameters
    ----------
    *args : array
        1: team name, 
        2: player discord id

    Raises
    ------

    """


    try:
        db.deleteMember(args[0], re.sub(r'[<@!>]', '', args[1]))
        await ctx.channel.send(args[1]+" is kicked from "+args[0])
    except:
        print(sys.exc_info())

#######################################################################

@client.command(name='series')
async def create_series(ctx, *args):
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
async def add_result(ctx, *args):
    """Takes series id and match replay to append its stats to the series

    Command
    ----------
    to add a new match to the series :
        ;result <series id> <replay link>

    Parameters
    ----------
    *args : array
        1: id of the series that was created, 
        2: replay link

    Raises
    ------
    not a valid replay
        if the replay link couldn't be downloaded or not a replay or it is corrupted 

    """

    matchID = args[0]

    try:
        replay = functions.download_replay(args[1])
        blue, orange = functions.parse_replay(replay)
        db.insertResult(matchID, blue, orange)
        await ctx.channel.send("match replay successfully added to the series")

    except:
        await ctx.channel.send('not a valid replay')
        return


#######################################################################

@client.command(name='stats')
async def stats(ctx, *args):
    players, teams, matches = db.exctractDataFrames()
    players.to_csv('players.csv')
    teams.to_csv('teams.csv')
    matches.to_csv('matches.csv')

#######################################################################

@client.command(name='pop')
async def remove_match(ctx, *args):
    """Takes series id and remove last added match

    Command
    ----------
    to remove last match from the series :
        ;result <series id>

    Parameters
    ----------
    *args : str
        id of the series that was created, 

    Raises
    ------
    series is already empty
        happens when trying to pop a series that has no matches

    """

    try:
        db.removeLastReplay(args[0])
        await ctx.channel.send("last match replay successfully remove from the series")

    except:
        await ctx.channel.send('series is already empty')
        return
    

#######################################################################

@client.command(name='commit')
async def update_player_stats(ctx, *args):
    """Takes series id and commits their stats to the players

    Command
    ----------
    to update players stats with the new series :
        ;commit <series id>

    Parameters
    ----------
    *args : str
        id of the series that was created

    Raises
    ------

    """

    try:
        db.commitSeries(args[0])
        await ctx.channel.send("Players stats were updated successfully")

    except:
        print(sys.exc_info())
        return

#######################################################################

@client.command(name='uncommit')
async def reset_player_stats(ctx, *args):
    """Takes series id and removes their stats from the players

    Command
    ----------
    to reset stats of players before a certain series:
        ;uncommit <series id>

    Parameters
    ----------
    *args : str
        id of the series that was created

    Raises
    ------

    """


    try:
        db.uncommitSeries(args[0])
        await ctx.channel.send("Players stats were reset")

    except:
        print(sys.exc_info())
        return

#######################################################################

@client.command(name='view')
async def get_series(ctx, *args):
    """Takes series id and returns it in the channel

    Command
    ----------
    to get series data:
        ;view <series id>

    Parameters
    ----------
    *args : str
        id of the series that was created

    Raises
    ------

    """


    try:
        date, df = db.getSeries(args[0])
        teams = list(df['Team'].unique())
        await ctx.channel.send('Series: '+str(teams[0]) + ' vs ' + str(teams[1]) + ' on: ' 
                                + str(date.day) + '/' + str(date.month) + ' ' + str(date.hour) + ':' + str(date.minute))
        for match in df['Game number'].unique():
            await ctx.channel.send('Game #'+str(match))
            await ctx.channel.send("```" + df[df['Game number'] == match].drop('Game number', axis=1).set_index('Player').to_string() + "```")

    except:
        await ctx.channel.send('series not found')
        return

    

#######################################################################
