import discord
import os
from chatbot import config, llm
from typing import Self
from discord.ext import commands
import logging

discord.utils.setup_logging()

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
            content="This is an edited button response!"
        )

    @discord.ui.button(label="Bad bot", style=discord.ButtonStyle.red)
    async def bad_button(
        self: Self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await interaction.response.send_message(
            content="This is an edited button response!"
        )


@bot.command(name="q")
async def query_llm(
    ctx: commands.Context,
    *,
    arg: str
):
    logging.info("Got message %s", arg)
    async with ctx.typing():
        response = await llm.query_llm(arg)
    await ctx.send(response)


def main():
    bot.run(os.environ["TOKEN"])


if __name__ == "__main__":
    main()
