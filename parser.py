import carball
import pandas as pd
import requests
from tabulate import tabulate
import json

def parse_replay(replay):
    j = carball.decompile_replay(replay)

    with open("sample.json", "w") as outfile: 
        json.dump(j, outfile, indent = 1)

    data = pd.DataFrame(j["properties"]['PlayerStats'])

    c = data.pop('Name')
    data.insert(0, c.name, c)

    c = data.pop('OnlineID')
    data.insert(0, c.name, c)

    c = data.pop('Goals')
    data.insert(2, c.name, c)

    c = data.pop('Score')
    data.insert(2, c.name, c)

    data.pop('Platform')
    data.pop('bBot')

    data['Team'] = data['Team'].apply(lambda x: 'O' if x == 1 else 'B')
    
    blue = data[data['Team'] == 'B']

    if len(blue) > 0:
        blue = blue.set_index('Team').sort_values('Score', ascending=False).to_string(index=False)

    else:
        blue = 'Team Left Early'

    
    orange = data[data['Team'] == 'O']

    if len(orange) > 0:
        orange = orange.set_index('Team').sort_values('Score', ascending=False).to_string(index=False)

    else:
        orange = 'Team Left Early'

    print(blue, orange)

#response = requests.get('https://cdn.discordapp.com/attachments/726075186474123306/861480216950210600/h.replay')

#open('f.replay', 'wb').write(response.content)

parse_replay('z.replay')