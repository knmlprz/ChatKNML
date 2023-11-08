import discord
import os
import config

from discord.ext import commands
from .llm import ask_model

intents = discord.Intents(messages=True)

bot = commands.Bot(command_prefix=config.PREFIX, help_command=None, intents=intents)

@bot.command(name="ask smol model")
async def _ask_smol_model(
    ctx: commands.Context,
    arg: str,
):
    return ask_model(arg, "smol")


@bot.command(name="ask big model")
async def _ask_big_model(
    ctx: commands.Context,
    arg: str,
):
    return ask_model(arg, "big")


bot.run(os.environ["TOKEN"])

bot.add_command(_ask_smol_model)
bot.add_command(_ask_big_model)
