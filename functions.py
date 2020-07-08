import pyshorteners
from prettytable import PrettyTable
from crop import crop_stats
from spreed_sheet import insert_stats, create_worksheet

import pytesseract
import os
import re
import math
from PIL import Image, ImageEnhance, ImageOps


import requests
from io import BytesIO
import numpy as np

def download_image(link):

    response = requests.get(link)
    img = Image.open(BytesIO(response.content))
    img.save('matches/Match.png')

    return 'matches/Match.png'

def extract_stats_from_image(f):
    im = Image.open(f)
    enhancer = ImageEnhance.Color(ImageOps.invert(im.convert('RGB')))
    im = enhancer.enhance(0)

    pixels = im.load()

    for i in range(im.size[0]):    # for every col:
        for j in range(im.size[1]):    # For every row
            if pixels[i,j][0] > 180: # set the colour accordingly
                pixels[i, j] = (255, 255, 255)
            else:
                pixels[i, j] = (0, 0, 0)

    custom_config = '--psm 4'
    data = pytesseract.image_to_string(im, config = custom_config)
    prettydata = re.sub(r'\s+', ' ', data)

    return prettydata

def prettyfy_stats(data, worksheet, game_number):
    data = data.split(" ")

    score = data[0 : 3]
    goals = data[3 : 6]
    assists = data[6 : 9]
    saves = data[9 : 12]
    shots = data[12 : 15]

    remove_alphabets(score)
    remove_alphabets(goals)
    remove_alphabets(assists)
    remove_alphabets(saves)
    remove_alphabets(shots)

    #send the data to the spread sheet to be inserted
    insert_stats(worksheet, game_number, score, goals, assists, saves, shots)

    table = PrettyTable()
    table.field_names = ["Score", "Goals", "Assists", "Save", 'Shots']

    for i in range(3):
        table.add_row([score[i], goals[i], assists[i], saves[i], shots[i]])
        
    return table

def remove_alphabets(arr):
    num = ""

    for i in range(3):
        try: 
            num = num + str(int(arr[i]))
            arr[i] = num

        except:
            for x in arr[i]:
                try:
                    num = num + str(int(x))

                except:
                    num = num + "0"

            arr[i] = num

        num = ""
    

def get_stats(f, game_number, link):
    #crop the stats out of the full image
    img1, img2 = crop_stats(f)

    #extract the stats from the cropped images
    team_1_stats = extract_stats_from_image(img1)
    team_2_stats = extract_stats_from_image(img2)

    #create the worksheet for the stats
    ws = create_worksheet(link)

    #remove any Alphabets that were read instead of zero
    team_1_stats = prettyfy_stats(team_1_stats, ws, game_number)
    team_2_stats = prettyfy_stats(team_2_stats, ws, game_number)

    return team_1_stats, team_2_stats