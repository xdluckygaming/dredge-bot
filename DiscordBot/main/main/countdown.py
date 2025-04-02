import discord
from discord.ext import commands
import asyncio
from discord import user
from discord import FFmpegPCMAudio
import requests
import json

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def countdown(ctx, start=10):
    """
    Command to initiate a countdown in the Discord chat.

    Parameters:
    - ctx: discord.ext.commands.Context
        The context object representing the invocation context of the command.
    - start: int, optional
        The starting number for the countdown. Default is 10.

    Returns:
    - None

    Raises:
    - discord.ext.commands.CommandInvokeError:
        Raised if there is an error while sending messages to the Discord chat.
    """

    # Checking if the start value is a positive integer
    if not isinstance(start, int) or start <= 0:
        await ctx.send("Invalid start value. Please provide a positive integer.")
        return

    # Sending the initial message
    message = await ctx.send(start)

    # Countdown loop
    while start > 0:
        await asyncio.sleep(1)  # Wait for 1 second
        start -= 1
        await message.edit(content=start)

    await ctx.send("Countdown complete!")

bot.run('MTM0NDA0NDAzOTMwNTE2Njg0OA.GznRZ2.TpPUUg3HW-xcVr0uOPAubUU0oSj8312Pe5sXsU')