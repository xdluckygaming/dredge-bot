import discord
import asyncio
import os
import json
import requests
from discord.ext import commands
from discord import user
from discord import FFmpegPCMAudio

client = commands.Bot(command_prefix = '!',intents=discord.Intents.all())

intents = discord.Intents.default()
intents.members = True

@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('Dredge_locker_reach_and_exit.ogg')
        player = voice.play(source)

class MyBot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_voice_state_update(self, member, before, after):
        # We want to check when the bot itself joins a voice channel
        if member == self.user:  # Check if the event is for the bot
            if before.channel is None and after.channel is not None:
                # Bot has joined a new voice channel
                print(f"Bot joined the voice channel: {after.channel.name}")
                await self.start_countdown(after.channel)
            elif after.channel is None:
                # Bot has left the voice channel
                print(f"Bot left the voice channel.")
            else:
                # Bot has moved between voice channels
                print(f"Bot moved from {before.channel.name} to {after.channel.name}")

    async def start_countdown(self, channel):
        # Send countdown messages to a text channel (using the first text channel for simplicity)
        text_channel = channel.guild.text_channels[0]  # You can customize this to target a specific text channel
        countdown_time = 10  # Set the countdown time in seconds

        # Start sending countdown messages
        while countdown_time > 0:
            await text_channel.send(f"Countdown: {countdown_time} seconds remaining.")
            await asyncio.sleep(1)  # Wait for 1 second
            countdown_time -= 1

        # Send a message when the countdown is over
        await text_channel.send("Countdown finished! Playing audio now...")

        # After countdown finishes, play audio in the voice channel
        await self.play_audio(channel)

    async def play_audio(self, channel):
        # Ensure the bot is connected to the voice channel
        voice_channel = channel
        if not voice_channel:
            return

        print("Bot is connecting to the voice channel...")
        # Connect to the voice channel
        voice_client = await voice_channel.connect()

        # Set the path to your audio file (ensure the path is correct)
        audio_source = discord.FFmpegPCMAudio("path/to/your/audio/file.mp3")

        # Play the audio
        voice_client.play(audio_source, after=lambda e: print(f'Finished playing: {e}'))

        # Wait for the audio to finish playing
        while voice_client.is_playing():
            await asyncio.sleep(1)

        # After audio finishes, disconnect the bot from the voice channel
        print("Audio finished playing, disconnecting the bot.")
        await voice_client.disconnect()

client.run('MTM0NDA0NDAzOTMwNTE2Njg0OA.GznRZ2.TpPUUg3HW-xcVr0uOPAubUU0oSj8312Pe5sXsU')
