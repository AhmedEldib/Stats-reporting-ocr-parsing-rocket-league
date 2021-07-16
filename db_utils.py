import json
import pymongo
import datetime


def connect():
    from pymongo import MongoClient
    client = MongoClient(json.load(open("bot_creds.json"))["db"])
    db = client['statbot']
    return db


myDB = connect()


def insertNewPlayer(discord_id, name, mobile_number, rank, rocket_id, online_id='$', total_score=0, total_games=0, total_goals=0, total_assists=0, total_saves=0, total_shots=0):
    doc = {'_id': discord_id, 'name': name, 'mobile_number': mobile_number, 'rank': int(rank), 'rocket_id': rocket_id, 'online_id': online_id, 'total_score': total_score,
           'total_games': total_games, 'total_goals': total_goals, 'total_assists': total_assists, 'total_saves': total_saves, 'total_shots': total_shots}

    current_collection = myDB['players']
    current_collection.create_index(
        [("name", pymongo.DESCENDING)], unique=True)
    current_collection.create_index(
        [("rocket_id", pymongo.DESCENDING)], unique=True)

    current_collection.insert(doc)


def insertTeam(teamName, captain, player_2, player_3):
    doc = {'_id': teamName, 'captain': captain,
           'player_2': player_2, 'player_3': player_3}

    current_collection = myDB['Teams']
    current_collection.create_index(
        [("captain", pymongo.DESCENDING), ("player_2", pymongo.DESCENDING), ("player_3", pymongo.DESCENDING)], unique=True)

    current_collection.insert(doc)


def insertMatch(date, time, team1, team2):
    date_array = date.split('-')
    time_array = time.split(':')
    date_time = datetime.datetime(
        int(date_array[2]), int(date_array[1]), int(date_array[0]), int(time_array[0]), int(time_array[1]))

    doc = {'played': 0, 'date': date_time, 'team1': team1,
           'team2': team2, 'team1_goals': 0, 'team2_goals': 0, 'player1_score': 0, 'player1_goals': 0, 'player1_assists': 0, 'player1_shots': 0, 'player1_saves': 0, 'player2_score': 0, 'player2_goals': 0, 'player2_assists': 0, 'player2_shots': 0, 'player2_saves': 0, 'player3_score': 0, 'player3_goals': 0, 'player3_assists': 0, 'player3_shots': 0, 'player3_saves': 0, 'player4_score': 0, 'player4_goals': 0, 'player4_assists': 0, 'player4_shots': 0, 'player4_saves': 0, 'player5_score': 0, 'player5_goals': 0, 'player5_assists': 0, 'player5_shots': 0, 'player5_saves': 0, 'player6_score': 0, 'player6_goals': 0, 'player6_assists': 0, 'player6_shots': 0, 'player6_saves': 0}
    current_collection = myDB['matches']
    current_collection.insert(doc)
