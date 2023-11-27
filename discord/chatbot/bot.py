import discord
import os
from chatbot import config
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
        logging.info(interaction.message.content)
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


@bot.command()
async def pomocy(
    ctx: commands.Context,
    *args: str,
):
    await ctx.send(args, view=Buttons())


def main():
    bot.run(os.environ["TOKEN"])


if __name__ == "__main__":
    main()
