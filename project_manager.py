from bot_initialization import client
import re

#*********************** rocket stats *************************
@client.event
async def on_message(message):
    if str(message.author.id) != '535120412724690955':
        try:
            img = functions.download_image(message.attachments[0].url)
            team_1, team_2 = functions.get_stats(img)
            await message.channel.send("TEAM 1 \n" + "``` " + str(team_1) + " ``` \n" + "TEAM 2 \n" + "``` " + str(team_2) + " ```")

        except:
            try:
                img = functions.download_image(message.content)
                team_1, team_2 = functions.get_stats(img)
                await message.channel.send("TEAM 1 \n" + "``` " + str(team_1) + " ``` \n" + "TEAM 2 \n" + "``` " + str(team_2) + " ```")

            except:
                print('not an image')
                return