import discord
from discord.ext import commands


intents = discord.Intents.all()


client = commands.Bot(command_prefix="!", help_command=None, intents=intents)

client.run()
