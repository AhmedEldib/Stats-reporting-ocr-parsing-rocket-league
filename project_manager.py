from bot_initialization import client
import functions
import re
from spreed_sheet import create_worksheet

spreedsheet_link = []
spreedsheet_link.append("ur Spreadsheet link here with edit permission")

#*********************** rocket stats *************************
@client.command(name = 'a')
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
        team_1, team_2 = functions.get_stats(img, game_number, spreedsheet_link[0])
        await ctx.channel.send("TEAM 1 \n" + "``` " + str(team_1) + " ``` \n" + "TEAM 2 \n" + "``` " + str(team_2) + " ```" + "\n The stats can be found here : " + spreedsheet_link[0])

    except:
        await ctx.channel.send('Invalid Image')
        return

@client.command(name = 's')
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