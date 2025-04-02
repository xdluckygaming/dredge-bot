import discord
from discord.ext import commands
from discord import user
from discord import FFmpegPCMAudio
import requests
import json

client = commands.Bot(command_prefix = '!',intents=discord.Intents.all())

intents = discord.Intents.default()
intents.members = True


async def play_file(ctx, param):
    pass


@client.command()
@client.guild_only()
async def command_syntax(self, ctx):
    """command_description"""
    await play_file(ctx, 'AudioEvent_NightTime_NearActivation_Warning.ogg')

client.run('MTM0NDA0NDAzOTMwNTE2Njg0OA.GznRZ2.TpPUUg3HW-xcVr0uOPAubUU0oSj8312Pe5sXsU')