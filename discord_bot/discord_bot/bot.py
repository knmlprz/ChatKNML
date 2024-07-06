import asyncio
import discord
import functools
import json
import os
import requests
import typing
from collections import defaultdict
from discord.ext import commands
from http import HTTPStatus
from typing import Self

from discord_bot import config

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config.PREFIX, help_command=None, intents=intents)


async def get_chats_history():
    """Taking chat conversation from all channels."""
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
@commands.has_any_role("Admins", "Moderators")
async def sync(ctx) -> None:
    """Call to Discord API to update slash commands."""
    await ctx.send("Synchronizing commands...")
    await bot.tree.sync()


def query_llm(prompt):
    """Returns llm's response."""
    url = "http://192.168.0.1:8000/api/bot/"
    headers = {"Content-Type": "application/json"}
    data = {"input": prompt}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == HTTPStatus.OK:
        print("fdafhdfh")
        return response.json()['output']

    return response.text


@bot.command()
async def show(ctx: commands.Context, limit: int = 100):
    """Shows the results of get_chats_history."""
    last_messages = await get_chats_history()
    channel_id = ctx.channel.id
    if last_messages[channel_id]:
        for msg in last_messages[channel_id][:limit]:
            await ctx.send(msg)
    else:
        await ctx.send("Brak ostatnich wiadomości.")


@bot.command(name="chatknml", description="Porozmawiaj z chatbotem")
async def chatknml(ctx: commands.Context, *, prompt: str):
    """Passes the prompt to the llm and returns the answer."""
    result = query_llm(prompt)
    await ctx.send("HEJ" + result)


def main():
    """Entrypoint."""
    bot.run(os.environ["TOKEN"])


if __name__ == "__main__":
    main()
