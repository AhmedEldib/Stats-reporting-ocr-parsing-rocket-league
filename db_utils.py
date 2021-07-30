import json
import pymongo
import datetime
from bson.objectid import ObjectId
import uuid


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


def insertNewPlayer(discord_id, name, mobile_number, rank, rocket_id, online_id='$', total_score=0, total_games=0, total_goals=0, total_assists=0, total_saves=0, total_shots=0):
    doc = {'_id': discord_id, 'name': name, 'mobile_number': mobile_number, 'rank': int(rank), 'rocket_id': rocket_id, 'online_id': online_id, 'total_score': total_score,
           'total_games': total_games, 'total_goals': total_goals, 'total_assists': total_assists, 'total_saves': total_saves, 'total_shots': total_shots}

    current_collection = myDB['players']
    current_collection.create_index(
        [("name", pymongo.DESCENDING)], unique=True)
    current_collection.create_index(
        [("rocket_id", pymongo.DESCENDING)], unique=True)

    current_collection.insert(doc)


def insertTeam(teamName, captain, player_2, player_3, sub=None):
    doc = {'_id': teamName, 'captain': captain,
           'player2': player_2, 'player3': player_3, 'sub': sub}

    current_collection = myDB['teams']
    current_collection.create_index(
        [("captain", pymongo.DESCENDING), ("player2", pymongo.DESCENDING), ("player3", pymongo.DESCENDING)], unique=True)

    current_collection.insert(doc)


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
           'team2': team2, 'team1_goals': 0, 'team2_goals': 0, 'player1_id': team1_players[team1['who'][0]], 'player1_score': 0, 'player1_goals': 0, 'player1_assists': 0, 'player1_shots': 0, 'player1_saves': 0, 'player2_id': team1_players[team1['who'][1]], 'player2_score': 0, 'player2_goals': 0, 'player2_assists': 0, 'player2_shots': 0, 'player2_saves': 0, 'player3_id': team1_players[team1['who'][2]], 'player3_score': 0, 'player3_goals': 0, 'player3_assists': 0, 'player3_shots': 0, 'player3_saves': 0, 'player4_id': team2_players[team2['who'][0]], 'player4_score': 0, 'player4_goals': 0, 'player4_assists': 0, 'player4_shots': 0, 'player4_saves': 0, 'player5_id': team2_players[team2['who'][1]], 'player5_score': 0, 'player5_goals': 0, 'player5_assists': 0, 'player5_shots': 0, 'player5_saves': 0, 'player6_id': team2_players[team2['who'][2]], 'player6_score': 0, 'player6_goals': 0, 'player6_assists': 0, 'player6_shots': 0, 'player6_saves': 0}

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
        currentPlayerID = matchDictionary['player'+str(i)+'_id']
        currentPlayer = playerCollection.find_one({'_id': currentPlayerID})
        currentTeam = team1 if i < 4 else team2
        currentPlayerStats = currentTeam[currentTeam['Name']
                                         == currentPlayer['name']].values[0]

        # Updating player info
        if currentPlayer['online_id'] == '$':
            currentPlayer['online_id'] = currentPlayerStats[statsDictionary['OnlineID']]

        currentPlayer['total_score'] += currentPlayerStats[statsDictionary['Score']]
        currentPlayer['total_goals'] += currentPlayerStats[statsDictionary['Goals']]
        currentPlayer['total_assists'] += currentPlayerStats[statsDictionary['Assists']]
        currentPlayer['total_saves'] += currentPlayerStats[statsDictionary['Saves']]
        currentPlayer['total_shots'] += currentPlayerStats[statsDictionary['Shots']]
        currentPlayer['total_games'] += 1

        playerCollection.update({"_id": currentPlayer['_id']}, {
                                '$set': currentPlayer}, upsert=False)

        # Updating match info
        matchDictionary['player' +
                        str(i)+'_score'] = currentPlayerStats[statsDictionary['Score']]
        matchDictionary['player' +
                        str(i)+'_goals'] = currentPlayerStats[statsDictionary['Goals']]
        matchDictionary['player' +
                        str(i)+'_assists'] = currentPlayerStats[statsDictionary['Assists']]
        matchDictionary['player' +
                        str(i)+'_shots'] = currentPlayerStats[statsDictionary['Shots']]
        matchDictionary['player' +
                        str(i)+'_saves'] = currentPlayerStats[statsDictionary['Saves']]

        team1_goals += currentPlayerStats[statsDictionary['Goals']
                                          ] if i < 4 else 0
        team2_goals += currentPlayerStats[statsDictionary['Goals']
                                          ] if i >= 4 else 0

    matchDictionary['team1_goals'] = team1_goals
    matchDictionary['team2_goals'] = team2_goals

    matchCollection.update({"_id": matchDictionary['_id']}, {
        '$set': matchDictionary}, upsert=False)
