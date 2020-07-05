import discord
from discord.ext import commands

certificate = 'C:\\Users\\DELL\\Anaconda3\\lib\\site-packages\\certifi\\cacert.pem'

client = commands.Bot(command_prefix = ';')

@client.event
async def on_ready():
    print('READY')
