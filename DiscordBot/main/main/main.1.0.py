import discord
from discord import app_commands
from discord import user
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands import MissingPermissions
from dotenv import load_dotenv
from yt_dlp import YoutubeDL
import requests
import json
import asyncio
import os

load_dotenv(dotenv_path='.env')
dredge_token = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix = '!',intents=discord.Intents.all())

intents = discord.Intents.default()
intents.members = True

queues = {}

def check_queue(ctx, id):
    if queues[id] != []:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        player = voice.play(source)

@client.event
async def on_ready():
    try:
        synced = await client.tree.sync()
        print(f"synced {len(synced)} commands.")
    except Exception as e:
        print(f"Error syncing commands: {e}")
    print(f"logged in as {client.user}")

@client.command()
async def hello(ctx):
    await ctx.send("the dredge looks your way")

@client.command()
async def goodbye(ctx):
    await ctx.send("dredge teleports away")

@client.event
async def on_member_join(member):
    channel = client.get_channel(1270738951287603286)
    await channel.send(f"Dredge welcomes {member} into the fog ")

@client.event
async def on_member_remove(member):
    channel = client.get_channel(1270738951287603286)
    await channel.send(f"dredge teleports {member} away")

@client.command(pass_context = True)
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("dredge teleported away")
    else:
        await ctx.send("dredge is not in a locker (voice channel)")

@client.command(pass_context = True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("dredge is silent right now")

@client.command(pass_context = True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("dredge doesnt have audio paused")

@client.command(pass_context = True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()

@client.command(pass_context = True)
async def play(ctx, arg):
    voice = ctx.guild.voice_client
    source = FFmpegPCMAudio(arg + '.ogg')
    player = voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id))

@client.command(pass_context = True)
async def queue(ctx, arg):
    voice = ctx.guild.voice_client
    source = FFmpegPCMAudio(arg + '.ogg')

    guild_id = ctx.message.guild.id

    if guild_id in queues:
        queues[guild_id].append(source)

    else:
        queues[guild_id] = [source]

    await ctx.send("added to queue")

@client.command(pass_context = True)
async def activate_nightfall(ctx):
    voice = ctx.guild.voice_client
    source = FFmpegPCMAudio("Nightfall_Entirety.ogg")
    player = voice.play(source)

@client.command(pass_context = True)
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if channel.guild.voice_client is None:
            voice = await channel.connect()
            source = FFmpegPCMAudio('Dredge_locker_reach_and_exit.ogg')
            voice.play(source)
        else:
            await ctx.send("dredge is already in locker (voice channel)")
    else:
        await ctx.send("survivor must enter locker (voice channel) first")

@client.event
async def on_voice_state_update(member,before,after):
    if after.channel and after.channel.guild.me == member:
        print(f"Bot joined the channel: {after.channel.name}")
        text_channel = find_text_channel(after.channel)
        if text_channel:
            await start_countdown(text_channel)


@client.event
async def start_countdown(channel, countdown_time=102, audio_file="AudioEvent_NightTime_NearActivation_Warning.ogg"):
    while countdown_time > 0:
        print(f"Countdown: {countdown_time} seconds remaining.")
        await asyncio.sleep(1)
        countdown_time -= 1

    await channel.send("nightfall activates soon")
    await play_audio(channel, audio_file)

    second_countdown_time = 18
    second_audio_file = "Nightfall_entirety.ogg"

    print(f"nightfall almost activates in {second_countdown_time} seconds")
    await start_second_countdown(channel, second_countdown_time, second_audio_file)

@client.event
async def start_second_countdown(channel, countdown_time, audio_file):
    while countdown_time > 0:
        print(f"Second Countdown: {countdown_time} seconds remaining.")
        await asyncio.sleep(1)
        countdown_time -= 1
    print(f"second countdown complete, playing audio")
    await channel.send ("nightfall is upon you")
    await play_audio2(channel, audio_file)

@client.event
async def play_audio(channel, audio_file):
    if not channel.guild.voice_client:
        return
    voice_client = channel.guild.voice_client

    audio_source = FFmpegPCMAudio("AudioEvent_NightTime_NearActivation_Warning.ogg")
    voice_client.play(audio_source, after=lambda e: print(f'Finished playing: {e}'))

    while voice_client.is_playing():
        await asyncio.sleep(1)

@client.event
async def play_audio2(channel, audio_file):
    if not channel.guild.voice_client:
        return
    voice_client = channel.guild.voice_client

    audio_source2 = FFmpegPCMAudio("Nightfall_Entirety.ogg")
    voice_client.play(audio_source2, after=lambda e: print(f'Finished playing: {e}'))

    while voice_client.is_playing():
        await asyncio.sleep(1)

def find_text_channel(voice_channel, target_channel_name="bot-commands"):
    for channel in voice_channel.guild.text_channels:
        if channel.name == target_channel_name:
            return channel
    return None

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "sadako sucks" in message.content.lower():
        await message.delete()
        await message.channel.send("dredge dissaproves of this, dont send again or dredge will take you into the fog")

    await client.process_commands(message)

@client.tree.command(name="kick", description="kidnaps user into fog (kicks member of server)")
@app_commands.describe(member = "member to kick", reason = "reason to kick user")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "no reason provided"):
    try:
        await member.kick(reason=reason)
        await interaction.response.send_message(f'User {member} was forced out of the exit gates by dredge (member got kicked for {reason})')
    except discord.Forbidden:
        await interaction.response.send_message(f"dredge cant kidnap {member} because he isn't strong enough (no permissions)", ephermeral=True)
    except Exception as e:
        await interaction.response.send_message(f"An error has occurred: {e}", ephemeral=True)

@client.tree.command(name="ban", description="Ban a member from the server")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.ban_members:
        return await interaction.response.send_message("❌ only entity can control dredge (no permission).", ephemeral=True)

    await member.ban(reason=reason)
    await interaction.response.send_message(f"🔨 {member.mention} has been taken to the void by dredge because: {reason}")

@client.tree.command(name="unban", description="Unban a user by their username")
async def unban(interaction: discord.Interaction, username: str):
    if not interaction.user.guild_permissions.ban_members:
        return await interaction.response.send_message("❌ dredge only listens to entity (no permissions).", ephemeral=True)

    try:
        banned_user = None
        async for ban_entry in interaction.guild.bans():
            if ban_entry.user.name.lower() == username.lower():
                banned_user = ban_entry.user
                break

        if banned_user:
            # Unban the user
            await interaction.guild.unban(banned_user)
            return await interaction.response.send_message(f"✅ {banned_user.mention} has escaped the void.")

        await interaction.response.send_message("❌ Dredge hasn't taken that user.", ephemeral=True)

    except discord.Forbidden:
        await interaction.response.send_message("❌ dredge cant unban that user", ephemeral=True)

@client.tree.command(name="play", description="{play audio from Youtube or Spotify")
@app_commands.describe(url="The URL of the audio to play")
async def play_stream(interaction: discord.Interaction, url:str):

    if interaction.user.voice is None:
        await interaction.response.send_message("Dredge doesnt see you in the realm (vc)", ephemeral=True)
        return

    channel = interaction.user.voice.channel
    if interaction.guild.voice_client is None:
        await channel.connect()

    voice_client = interaction.guild.voice_client

    try:
        await interaction.response.defer()
        YDL_OPTIONS = {
            'format': 'bestaudio',
            'noplaylist': True,
            'quiet': True,
            'extract_flat': True,
            'default_search': 'ytsearch'
        }
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn',
        }

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']
            title = info.get('title','unknown title')

        if voice_client.is_playing():
            voice_client.stop()

        voice_client.play(discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS))
        await interaction.followup.send(f"Dredge is now playing: {title}")
    except Exception as e:
        await interaction.followup.send(f"Dredge failed to play audio because: {e}", ephemeral=True)
@client.tree.command(name="stop", description="Stops Dredge from playing audio")
async def stop(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client and voice_client.is_playing():
        voice.client.stop()
        await interaction.response.send_message("playback Stopped.")
    else:
        await interaction.response.send_message("No audio is currently playing.", ephemeral=True)

client.run(dredge_token)