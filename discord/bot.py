import discord
import os
import config

from typing import Self
from discord.ext import commands

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=config.PREFIX, help_command=None, intents=intents)


class Buttons(discord.ui.View):
    def __init__(self: Self, *, timeout: int = 180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Good bot", style=discord.ButtonStyle.green)
    async def good_button(
        self: Self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await interaction.response.send_message(
        )



    @discord.ui.button(label="Bad bot", style=discord.ButtonStyle.red)
    async def bad_button(
        self: Self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await interaction.response.send_message(
        )



import asyncio
from collections import defaultdict
async def get_chats_history(bot):
    chats_history = defaultdict(list)
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).read_messages:
                async for message in channel.history(limit=100):
                    chats_history[channel.id].append(f"{message.author.name}: {message.content}")
    return chats_history
                    
                                    
bot.run("MTE3NTUwNDAwMTc4NjE4NzgxNg.GPMwqY.Sm3nWVukPsQhF3eeAdKQWVaLSPgrJZj2qSHCW8")

