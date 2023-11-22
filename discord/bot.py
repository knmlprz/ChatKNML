import discord
import os
import config
import logging

from discord.ext import commands
from llm import ask_model

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=config.PREFIX, help_command=None, intents=intents)

@bot.command(name="big")
async def big(
    ctx: commands.Context,
    *,
    arg: str,
):
    logger.info("Got ask_big_model command")
    async with ctx.typing():
        response = await ask_model(arg, "big")
    await ctx.send(response)



logger.warn("Hello")
bot.run(os.environ["TOKEN"])

