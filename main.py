# discord bot app
# https://realpython.com/how-to-make-a-discord-bot-python/#connecting-a-bot
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
# import random
from minigames import roll_dice, gacha_game, check_last_gacha, NPC_name, get_gacha_loot
# from item_finder import find_item
import time
from item_finder import find_item_easy

load_dotenv()
Token = os.getenv('DISC_TOKEN')
Server = os.getenv('DISC_SERVER')

bot = commands.Bot(command_prefix="Xime pls ")

@bot.event
async def on_ready():
    print("Bot online.")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='"Xime pls help"'))


@bot.command(name="find", help="> Finds D&D info. Use: Xime pls find item:name-of-item")
async def bot_find(ctx, item_name):
    print("Looking up item")
    # found = find_item(user_input=arg)
    found = find_item_easy(item_name)
    if found:
        for i in found:
            await ctx.send(i)
    else:
        await ctx.send("No item with that name found.\n**Use:** ``Xime pls find <item:name-of-item>``\n "
                       "works best for spell:name, item:name, feat:name and <class>:subclass")

@bot.command(name="do", help="> Does things? Maybe?")
async def do(ctx, arg="nothing"):
    await ctx.send(f"Doing {arg}.:thumbsup:")


@bot.command(name="name", help="> Thinks of a name for you!")
async def name(ctx, race):
    if not NPC_name(race):
        await ctx.send(f"{race} is not a valid entry, sorry. Use: ``Xime pls name <D&D race>``")
    else:
        new_name = NPC_name(race)
        await ctx.send(f"Your {race} is named {new_name}.")


@bot.command(name="gacha", help="> Let's you play a gacha game! Go get the rarest one!")
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
