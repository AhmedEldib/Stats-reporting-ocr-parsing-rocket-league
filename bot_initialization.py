import discord
from discord.ext import commands
import db_utils as db
# cretifacte to be able to use dicordApi
# needs to be downloaded and inserted in the same path
certificate = 'C:\\Users\\DELL\\Anaconda3\\lib\\site-packages\\certifi\\cacert.pem'

client = commands.Bot(command_prefix=';')


