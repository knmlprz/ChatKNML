import discord
import os
import config

from discord.ext import commands

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=config.PREFIX, help_command=None, intents=intents)


class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Good bot", style=discord.ButtonStyle.green)
    async def good_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message(
            content="This is an edited button response!"
        )

    @discord.ui.button(label="Bad bot", style=discord.ButtonStyle.red)
    async def bad_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message(
            content="This is an edited button response!"
        )


@bot.command()
async def ask(ctx, *args):
    await ctx.send(args, view=Buttons())


bot.run(os.environ.get("TOKEN", ""))
