"""Sets up discord bot."""

import os
from collections import defaultdict
from typing import Self

import discord
from discord.ext import commands

from discord_bot import config

intents = discord.Intents.default()
intents.message_content = True

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
            content="This is an edited button response!",
        )

    @discord.ui.button(label="Bad bot", style=discord.ButtonStyle.red)
    async def bad_button(
        self: Self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await interaction.response.send_message(
            content="This is an edited button response!",
        )


async def get_chats_history():
    """Taking chat conversation from all chanells."""
    chats_history = defaultdict(list)
    for guild in bot.guilds:
        readable_channels = filter(
            lambda c: c.permissions_for(guild.me).read_messages,
            guild.text_channels,
        )
        for channel in readable_channels:
            async for message in channel.history(limit=100):
                chats_history[channel.id].append(
                    f"{message.author.name}: {message.content}",
                )
    return chats_history


@bot.command()
async def show(ctx: commands.Context, limit: int = 100):
    """Shows what get_chats_history gets."""
    last_messages = await get_chats_history()
    channel_id = ctx.channel.id
    if last_messages[channel_id]:
        for msg in last_messages[channel_id][:limit]:
            await ctx.send(msg)
    else:
        await ctx.send("Brak ostatnich wiadomości.")


def main():
    """Entrypoint."""
    bot.run(os.environ["TOKEN"])


if __name__ == "__main__":
    main()
