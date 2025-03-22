import discord
import os
import datetime
from pathlib import Path
import requests

allowed_filetypes = (".mp4", ".MP4", ".gif", ".GIF", ".png", ".PNG", ".jpg", ".JPG", ".jpeg", ".JPEG", ".mov", ".MOV", ".webp", ".WEBP", ".webm", ".WEBM")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    customStatus = discord.CustomActivity(name="Checking the date")
    await client.change_presence(status=discord.Status.online, activity=customStatus)

    date_channel = client.get_channel(CHANNEL_ID_HERE)
    current_date = datetime.datetime.now().strftime("%b-%d")
    current_hour = datetime.datetime.now().strftime("%H")

    files = os.listdir("./content")

    for file in files:
        date_of_file = Path(file).stem
        if date_of_file == current_date and current_hour == 00:
            discord_file = discord.File(Path("./content/" + file))
            await date_channel.send(file=discord_file, content="")

    print("Logged in")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!commands') or message.content.startswith('!help'):
        await message.channel.send('There is one command. Use `!add` followed by the date in format Mar-22 and attach the media to add it to the list\nFor example: `!add Aug-03`')
        return

    if message.content.startswith('!add'):
        if len(message.attachments) != 1:
            await message.channel.send('You need to attach some media m8')
            return
        elif Path(message.attachments[0].filename).suffix not in allowed_filetypes:
            await message.channel.send('File extention is not allowed')
            return
        else:
            file_stem = message.content.split()[1]

            file_extension = Path(message.attachments[0].filename).suffix

            file_name = "./content/" + file_stem + file_extension

            await message.attachments[0].save(fp=file_name)
            await message.channel.send('Okay it likely added :)')
			
client.run('BOT_TOKEN_HERE')
