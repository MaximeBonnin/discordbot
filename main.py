
# discord bot app
# https://realpython.com/how-to-make-a-discord-bot-python/#connecting-a-bot

import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
# import random
from minigames import roll_dice, gacha_game, check_last_gacha, NPC_name, get_gacha_loot
from item_finder import find_item
import time
import csv

load_dotenv()
Token = os.getenv('DISC_TOKEN')
Server = os.getenv('DISC_SERVER')

bot = commands.Bot(command_prefix="Xime pls ")

@bot.event
async def on_ready():
    print("Bot online.")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='"Xime pls help"'))


@bot.command(name="find", help="> Finds D&D info. Use: 'Xime pls find item:name-of-item'")
async def bot_find(ctx, arg):
    print("Looking up item")
    found = find_item(user_input=arg)
    if found:
        output = ""
        for i in found.items():
            output = output + f"**{i[0]}:** {i[1]} \n"
        await ctx.send(output)
    else:
        await ctx.send("No item with that name found.")

@bot.command(name="do", help="> Does things? Maybe?")
async def do(ctx, arg="nothing"):
    await ctx.send(f"Doing {arg}.:thumbsup:")


@bot.command(name="name", help="> Thinks of a name for you!")
async def do(ctx, race):
    if not NPC_name(race):
        await ctx.send(f"{race} is not a valid entry, sorry.")
    else:
        new_name = NPC_name(race)
        await ctx.send(f"Your {race} is named {new_name}.")


@bot.command(name="gacha", help="> Does things? Maybe?")
async def gacha(ctx):
    userID = str(ctx.author.id)
    current = time.time()
    wait = 3
    last_time = check_last_gacha(userID)
    since_last = round(current-last_time)

    if since_last < wait:
        await ctx.send(f"You have to {wait} seconds before you can play again. {wait-since_last} left.")
    else:
        gacha_loot = gacha_game(userID)
        # x = "ERROR"
        await ctx.send(f"You got the {gacha_loot}. All you loot can be viewed with 'loot' command.")

@bot.command(name="loot", help="> Displays gacha loot")
async def gacha_loot(ctx):
    userID = str(ctx.author.id)
    result = get_gacha_loot(userID)
    await ctx.send(f"{result}")


@bot.command(name="roll", help="> Rolls dice. Format: <number of dice>d<number of sides>+<additional> [Example: 1d20+4]")
async def roll(ctx, die="1d20+0"):
    output_sum, output, added = roll_dice(die)
    op = " +"
    if added < 0:
        op = " "
    await ctx.send(f"Rolled **{output_sum}** total    *dice: {output}{op}{added}*")

if __name__ == "__main__":
    bot.run(Token)
