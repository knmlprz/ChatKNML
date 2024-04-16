"""Sets up discord bot."""

import json
import os
from collections import defaultdict
from typing import Self

import discord
import requests
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


@bot.command()
@commands.has_any_role("Admins", "Moderators")
async def sync(ctx) -> None:
    """Call to Discord API to update slash commands."""
    await ctx.send("Synchronizing commands...")
    await bot.tree.sync()


def query_llm(prompt, stop_signs):
    """Returns llm's response."""
    url = "http://llm:9000/v1/completions"
    headers = {"Content-Type": "application/json"}
    data = {"prompt": prompt, "stop": stop_signs}

    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=5)

    respose_status_code = 200

    if response.status_code == respose_status_code:
        return response.json()

    return response.text


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
async def show(ctx: commands.Context, limit: int = 100):
    """Shows the results of get_chats_history."""
    last_messages = await get_chats_history()
    channel_id = ctx.channel.id
    if last_messages[channel_id]:
        for msg in last_messages[channel_id][:limit]:
            await ctx.send(msg)
    else:
        await ctx.send("Brak ostatnich wiadomości.")


@bot.tree.command(name="chatknml", description="Porozmawiaj z chatbotem")
async def chatknml(interaction: discord.Interaction, *, prompt: str):
    """Passes the prompt to the llm and returns the answer."""
    await interaction.response.defer()

    query = "\n\n### Instructions:\n" + prompt + "\n\n### Response:\n"
    stop_signs = ["\n", "###"]

    result = query_llm(query, stop_signs)

    await interaction.followup.send(result["choices"][0]["text"])


def main():
    """Entrypoint."""
    bot.run(os.environ["TOKEN"])


if __name__ == "__main__":
    main()
