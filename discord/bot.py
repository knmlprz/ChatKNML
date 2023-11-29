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
            content="This is an edited button response!"
        )
        filename = f"discord/private_chats/{interaction.user.id}.txt"
        with open(filename, "a") as file:
            file.write(f"1\n")
        self.stop()



    @discord.ui.button(label="Bad bot", style=discord.ButtonStyle.red)
    async def bad_button(
        self: Self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await interaction.response.send_message(
            content="This is an edited button response!"
        )
        filename = f"discord/private_chats/{interaction.user.id}.txt"
        with open(filename, "a") as file:
            file.write(f"0\n")
        self.stop()


@bot.command()
async def ask(
    ctx: commands.Context,
    *args: str,
):
    await ctx.send(args, view=Buttons())


# wywołanie bota i przejście do rozmowy prywatnej
@bot.command()
async def DM(ctx, *, message=None):
    if not isinstance(ctx.channel, discord.DMChannel):
        message = "Witam, w czym mogę pomóc"
        author = ctx.author
        await author.send(message)
    else:
        message = "Jesteś już w rozmowie prywatnej, w czym mogę pomóc"
        author = ctx.author
        await author.send(message) 

# odpowiedź na każde z pytań lorem ipsum
@bot.event
async def on_message(message):
    if (message.author.bot == False) and isinstance(message.channel, discord.DMChannel) and not message.content.startswith('!DM'): 
                response = "Lorem ipsum \n"
                await message.channel.send(response, view = Buttons())
                filename = f"discord/private_chats/{message.author.id}.txt"
                with open(filename, "a") as file:
                        file.write(f"{message.author.display_name} - {message.clean_content} \n")
                        file.write(f"odpowiedź bota {response} - ")
    
    await bot.process_commands(message)



bot.run("MTE3NTUwNDAwMTc4NjE4NzgxNg.GeJlgw.at5Pn28P4hiYlKssHgzNyz2l80oQIwOjIeMG_k")
