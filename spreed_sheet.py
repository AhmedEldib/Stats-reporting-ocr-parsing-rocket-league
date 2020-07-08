import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def create_worksheet(link):
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find the spreadsheet
    sheet = client.open_by_url(link)

    #try to find a worksheet first, if it wasn't found create a new one
    try:
        ws = sheet.get_worksheet(0)

    except:
        ws = sheet.add_worksheet(title = "stats", rows="1000", cols="20")

    return ws

def insert_stats(ws, game_number, score, goals, assists, saves, shots):
    #try:
    #Setting up the dataframe
    players = ["p", "p", "p"] #empty array to be filled manually in the spreadsheet
    dataframe = pd.DataFrame({'Players' : players, 'Score': score, 'Goals' : goals, 'Assists' : assists, 'Saves' : saves, 'Shots' : shots, "Game No." : game_number})

    #get the index of the 1st empty row
    row_index = next_available_row(ws)

    if row_index == "1":
        ws.update("A1:G1", [dataframe.columns.values.tolist()])
        row_index = int(row_index) + 1 

    # cell_title = "A" + str(row_index)
    # row_index = int(row_index) + 1 

    first_limit = "A" + str(row_index)
    second_limit = "G" + str(int(row_index) + 3)
    limit = first_limit + ":" + second_limit

    # ws.update(cell_title, "Game " + str(game_number))
    ws.update(limit, dataframe.values.tolist()) #[dataframe.columns.values.tolist()] + 
    
    # except:
    #     print("Worksheet Error")

def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)