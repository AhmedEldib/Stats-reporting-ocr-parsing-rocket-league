import json
import pymongo
import datetime
from bson.objectid import ObjectId
import uuid
import pandas as pd
import numpy as np


def connect():
    from pymongo import MongoClient
    client = MongoClient(json.load(open("bot_creds.json"))["db"])
    db = client['statbot']
    return db


myDB = connect()


def initializeDB():
    players = json.load(open("fakeData/players.json"))["players"]
    teams = json.load(open("fakeData/teams.json"))["teams"]
    matches = json.load(open("fakeData/matches.json"))["matches"]
    for player in players:
        insertNewPlayer(player['_id'], player['name'],
                        player['mobile_number'], player['rank'], player['rocket_id'])
    for team in teams:
        insertTeam(team['_id'], team['captain'],
                   team['player_2'], team['player_3'], team['sub'] if 'sub' in team else None)

    for match in matches:
        insertMatch(match["date"], match["time"],
                    match["team1"], match["team2"])


def insertNewPlayer(discord_id, name, mobile_number, rank, rocket_id, tracker_link="", 
                    online_id='$', total_score=0, total_games=0, total_goals=0, total_assists=0, total_saves=0, total_shots=0):
    doc = {'_id': discord_id, 'name': name, 'mobile_number': mobile_number, 'rank': int(rank),
           'rocket_id': rocket_id, 'tracker_link': tracker_link, 'online_id': online_id, 'total_score': total_score,
           'total_games': total_games, 'total_goals': total_goals, 'total_assists': total_assists, 'total_saves': total_saves, 'total_shots': total_shots}

    current_collection = myDB['players']
    current_collection.create_index(
        [("name", pymongo.DESCENDING)], unique=True)
    current_collection.create_index(
        [("rocket_id", pymongo.DESCENDING)], unique=True)

    current_collection.insert(doc)


def insertTeam(teamName, captain, player_2=None, player_3=None, sub=None):
    doc = {'_id': teamName, 'captain': captain,
           'player2': player_2, 'player3': player_3, 'sub': sub}

    current_collection = myDB['teams']
    current_collection.create_index(
        [("captain", pymongo.DESCENDING), ("player2", pymongo.DESCENDING), ("player3", pymongo.DESCENDING)], unique=True)

    current_collection.insert(doc)


def joinTeam(teamName, player, role):
    teamDictionary = myDB['teams'].find_one({'_id': teamName})
    teamDictionary[role] = player

    myDB['teams'].update({"_id": teamDictionary['_id']}, {
        '$set': teamDictionary}, upsert=False)


def deleteMember(teamName, player):
    teamDictionary = myDB['teams'].find_one({'_id': teamName})
    #currentPlayer = myDB['players'].find_one({'_id': player})['name']
    for key, value in teamDictionary.items():
        if value == player:
            teamDictionary[key] = None
    myDB['teams'].update({"_id": teamDictionary['_id']}, {
        '$set': teamDictionary}, upsert=False)


def insertMatch(date, time, team1, team2):
    date_array = date.split('-')
    time_array = time.split(':')
    date_time = datetime.datetime(
        int(date_array[2]), int(date_array[1]), int(date_array[0]), int(time_array[0]), int(time_array[1]))

    team1_players = myDB['teams'].find_one({'_id': team1['name']})
    team2_players = myDB['teams'].find_one({'_id': team2['name']})

    matchID = None
    isNewID = False
    while not isNewID:
        matchID = uuid.uuid4().hex
        isNewID = myDB['matches'].find_one({'_id': matchID}) is None
    doc = {"_id": matchID, 'played': 0, 'date': date_time, 'team1': team1,
           'team2': team2, 'team1_goals': [], 'team2_goals': [],
           'player1_id': team1_players[team1['who'][0]], 'player1_score': [], 'player1_goals': [], 'player1_assists': [], 'player1_shots': [], 'player1_saves': [],
           'player2_id': team1_players[team1['who'][1]], 'player2_score': [], 'player2_goals': [], 'player2_assists': [], 'player2_shots': [], 'player2_saves': [],
           'player3_id': team1_players[team1['who'][2]], 'player3_score': [], 'player3_goals': [], 'player3_assists': [], 'player3_shots': [], 'player3_saves': [],
           'player4_id': team2_players[team2['who'][0]], 'player4_score': [], 'player4_goals': [], 'player4_assists': [], 'player4_shots': [], 'player4_saves': [],
           'player5_id': team2_players[team2['who'][1]], 'player5_score': [], 'player5_goals': [], 'player5_assists': [], 'player5_shots': [], 'player5_saves': [],
           'player6_id': team2_players[team2['who'][2]], 'player6_score': [], 'player6_goals': [], 'player6_assists': [], 'player6_shots': [], 'player6_saves': []}

    current_collection = myDB['matches']
    current_collection.insert(doc)
    return matchID


def insertResult(matchID, team1, team2):
    statsDictionary = {'OnlineID': 0, 'Name': 1, 'Score': 2,
                       'Goals': 3, 'Assists': 4, 'Saves': 5, 'Shots': 6}
    matchCollection = myDB['matches']
    playerCollection = myDB['players']
    matchDictionary = matchCollection.find_one({"_id": matchID})
    team1_goals = 0
    team2_goals = 0

    for i in range(1, 7):
        # Getting player info
        currentTeam = team1 if i < 4 else team2
        currentPlayerID = matchDictionary['player'+str(i)+'_id']
        currentPlayer = playerCollection.find_one(
            {'_id': currentPlayerID})
        currentPlayerStats = currentTeam[currentTeam['Name']
                                         == currentPlayer['name']].values[0]
        # Updating player info
        if currentPlayer['online_id'] == '$':
            currentPlayer['online_id'] = currentPlayerStats[statsDictionary['OnlineID']]

        playerCollection.update({"_id": currentPlayer['_id']}, {
                                '$set': currentPlayer}, upsert=False)

        # Updating match info
        matchDictionary['player' +
                        str(i)+'_score'].append(currentPlayerStats[statsDictionary['Score']])
        matchDictionary['player' +
                        str(i)+'_goals'].append(currentPlayerStats[statsDictionary['Goals']])
        matchDictionary['player' +
                        str(i)+'_assists'].append(currentPlayerStats[statsDictionary['Assists']])
        matchDictionary['player' +
                        str(i)+'_shots'].append(currentPlayerStats[statsDictionary['Shots']])
        matchDictionary['player' +
                        str(i)+'_saves'].append(currentPlayerStats[statsDictionary['Saves']])

        team1_goals += currentPlayerStats[statsDictionary['Goals']
                                          ] if i < 4 else 0
        team2_goals += currentPlayerStats[statsDictionary['Goals']
                                          ] if i >= 4 else 0

    matchDictionary['team1_goals'].append(team1_goals)
    matchDictionary['team2_goals'].append(team2_goals)
    matchDictionary['played'] += 1

    matchCollection.update({"_id": matchDictionary['_id']}, {
        '$set': matchDictionary}, upsert=False)


def exctractDataFrames():
    return pd.DataFrame(list(myDB['players'].find())), pd.DataFrame(list(myDB['teams'].find())), pd.DataFrame(list(myDB['matches'].find()))


def removeLastReplay(matchID):
    matchCollection = myDB['matches']
    matchDictionary = matchCollection.find_one({"_id": matchID})

    for key, value in matchDictionary.items():
        if type(value) == type([None, None]):
            del matchDictionary[key][-1]

    matchDictionary['played'] -= 1
    matchCollection.update({"_id": matchDictionary['_id']}, {
        '$set': matchDictionary}, upsert=False)


def commitSeries(matchID):
    statsArray = ['score', 'goals', 'assists', 'saves', 'shots']
    playerCollection = myDB['players']
    matchCollection = myDB['matches']

    for i in range(1, 7):
        # Getting player info
        matchDictionary = matchCollection.find_one({"_id": matchID})
        currentPlayerID = matchDictionary['player'+str(i)+'_id']
        currentPlayer = playerCollection.find_one(
            {'_id': currentPlayerID})
        # Updating player info
        for stat in statsArray:
            currentPlayerstat = matchDictionary['player'+str(i)+'_'+stat]
            currentPlayer['total_'+stat] += int(np.sum(currentPlayerstat))
        currentPlayer['total_games'] += matchDictionary['played']
        playerCollection.update({"_id": currentPlayer['_id']}, {
                                '$set': currentPlayer}, upsert=False)


def uncommitSeries(matchID):
    statsArray = ['score', 'goals', 'assists', 'saves', 'shots']
    playerCollection = myDB['players']
    matchCollection = myDB['matches']

    for i in range(1, 7):
        # Getting player info
        matchDictionary = matchCollection.find_one({"_id": matchID})
        currentPlayerID = matchDictionary['player'+str(i)+'_id']
        currentPlayer = playerCollection.find_one(
            {'_id': currentPlayerID})
        # Updating player info
        for stat in statsArray:
            currentPlayerstat = matchDictionary['player'+str(i)+'_'+stat]
            currentPlayer['total_'+stat] -= int(np.sum(currentPlayerstat))
        currentPlayer['total_games'] -= matchDictionary['played']
        playerCollection.update({"_id": currentPlayer['_id']}, {
                                '$set': currentPlayer}, upsert=False)


def getSeries(matchID):
    series = myDB['matches'].find_one({"_id": matchID})
    playerCollection = myDB['players']
    df = pd.DataFrame(columns=['Player', 'Game number', 'Team', 'Team Goals', 'Score', 'Goals',
                               'Assists', 'Shots', 'Saves'])
    index = 0
    gamesNumber = len(series['team1_goals'])
    for game in range(gamesNumber):
        for player in range(1, 7):
            currentTeam = 'team1' if player < 4 else 'team2'
            currentPlayer = playerCollection.find_one(
                {'_id': series['player'+str(player)+'_id']})['name']
            df.loc[index] = (currentPlayer, game+1,
                             series[currentTeam]['name'], series[currentTeam+'_goals'][game], series['player'+str(player)+'_score'][game], series['player'+str(player)+'_goals'][game], series['player'+str(player)+'_assists'][game], series['player'+str(player)+'_shots'][game], series['player'+str(player)+'_saves'][game])
            index += 1
    return series['date'], df
