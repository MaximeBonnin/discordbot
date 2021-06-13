import random
import time
import json
from bs4 import BeautifulSoup
import requests

def roll_dice(die="1d20+0"):
    try:
        added = 0
        if die.count("+") > 0:
            die, added = die.split("+")
            added = int(added)
        elif die.count("-") > 0:
            added = die.split("-")[1]
            die = die.split("-")[0]
            added = -int(added)

    except ValueError:
        added = 0
        print("Missing value")
    num, dice = die.split("d")
    num = int(num)
    dice = int(dice)
    output = []
    for i in range(num):
        output.append(random.randint(1, dice))
    output_sum = sum(output) + added

    return output_sum, output, added

def create_user(userID):
    print(f"Registering {userID} as new user.")
    with open("users.json") as json_data:
        users = json.load(json_data)

    users[userID] = {
        "ID": userID,
        "Name": "",
        "LastGacha": 0,
        "GachaInv": {
            "Nothing useful": 0,
            "Basic Gacha": 0,
            "Better Gacha": 0,
            "Good Gacha": 0,
            "Very rare Gacha": 0,
            "The legendary Gacha": 0
        }
    }

    with open('users.json', 'w') as outfile:
        json.dump(users, outfile, indent=4)

def check_last_gacha(userID):
    with open("users.json") as json_data:
        users = json.load(json_data)

    try:
        return users[userID]["LastGacha"]
    except KeyError:
        create_user(userID)
        return 0


# print(check_last_gacha(142770908489187329))

def gacha_game(userID):
    chances = [
        ["Basic Gacha", "Better Gacha", "Good Gacha", "Very rare Gacha", "The legendary Gacha"],
        [3, 15, 50, 200, 1000],
    ]

    itemWon = "Nothing useful"
    for i in range(len(chances[0])):
        # out_of = chances[]
        if random.randint(1, chances[1][i]) == 1:
            itemWon = chances[0][i]

    with open("users.json") as json_data:
        users = json.load(json_data)

    try:
        x = users[userID]["GachaInv"][itemWon]
    except KeyError:
        print("No valid user.")
        create_user(userID)
        with open("users.json") as json_data:
            users = json.load(json_data)

    users[userID]["GachaInv"][itemWon] += 1
    users[userID]["LastGacha"] = time.time()

    with open('users.json', 'w') as outfile:
        json.dump(users, outfile, indent=4)

    return itemWon

def get_gacha_loot(userID):
    with open("users.json") as json_data:
        users = json.load(json_data)

    try:
        loot =  users[userID]["GachaInv"]
    except KeyError:
        create_user(userID)
        loot = users[userID]["GachaInv"]

    output = ""
    for option in loot.items():
        output = output + f"**{option[0]}:** {option[1]}\n"

    return output

def NPC_name(race="tiefling"):
    # use random fantasy name creator https://www.fantasynamegen.com/{race}/short/
    # works for: elf, human, orc, dwarf, dragon(medium sug.), demon(medium sug.), halfling=hobbit, goliath=barbarian
    races = {
        "dragonborn": "dragon",
        "half-orc": "orc",
        "half-elf": "elf",
        "tielfing": "demon",
        "goliath": "barbarian",
        "halfling": "hobbit"
    }

    if race not in races:
        return False

    my_url = "https://www.fantasynamegen.com/" + races[race] + "/short/"
    html = requests.get(my_url)
    page_soup = BeautifulSoup(html.content, "html.parser")
    containers = page_soup.findAll("div", {"id": "main"})

    return containers[0].li.text
