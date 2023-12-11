import discord
import os
import config
import asyncio
from typing import Self
from discord.ext import commands
from collections import defaultdict

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




async def get_chats_history():
    chats_history = defaultdict(list)
    for guild in bot.guilds:
        readable_channels = filter(
            lambda c: c.permissions_for(guild.me).read_messages,
            guild.text_channels
        )
        for channel in readable_channels:
            async for message in channel.history(limit=100):
                chats_history[channel.id].append(f"{message.author.name}: {message.content}")
    return chats_history



# a comand to check what returns get_chats_history
@bot.command()
async def show(ctx: commands.Context, limit: int = 100):
    last_messages = await get_chats_history()
    channel_id = ctx.channel.id
    if last_messages[channel_id]:
        for msg in last_messages[channel_id][:limit]:
            await ctx.send(msg)
    else:
        await ctx.send("Brak ostatnich wiadomości.")

bot.run("MTE3NTUwNDAwMTc4NjE4NzgxNg.G7aYQ6.tnkStSGPkkDw30-eVtn2aCFQ9dIeaSqy_yb-O4")

