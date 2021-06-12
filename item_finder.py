
import requests
from bs4 import BeautifulSoup
# item finder for discord bot

# format class:subclass

# items -> https://www.aidedd.org/dnd/om.php?vo=alchemy-jug
# should really use this https://5e.tools/items/alchemy-jug-dmg.html

categories = {
    "item": "om",
    "spell": "sorts",
    "monster": "monstres",
    "feat": "feats",
    "invocation": "eldritch-invocations"
}

def find_item(user_input="monster:ogre"):
    # user_input = input("item: \n>>> ")

    raw_input = user_input.lower().replace(" ", "-")
    search_cat, search_term = raw_input.split(":")
    # print(search_cat, search_term)

    URL = f'https://www.aidedd.org/dnd/{categories[search_cat]}.php?vo={search_term}'
    # print(URL)
    site = requests.get(URL)
    soup = BeautifulSoup(site.content, 'html.parser')

    try:

        content = soup.find(class_='bloc')

        itemName = content.find("h1").text
        # print(itemName)

        itemRarity = content.find("em").text
        # print(itemRarity)

        itemDescription = content.find(class_="description").text

        itemSource = content.find(class_="source").text
        itemSource = itemSource.split("› ")[1]

        found = {
            "Name": itemName,
            "Info": itemRarity,
            "Source": itemSource,
            "Description": itemDescription,
            "Image": "No image"
        }

        try:
            itemImg = content.find(class_="picture").find("amp-img")["src"]
            # itemImg = f"https://www.aidedd.org/dnd/images-om/{search_term}.jpg"
            found["Image"] = itemImg
        except AttributeError:
            print("No image found.")

        # print(found)

        return found
    except AttributeError:
        print("Oops, no item found here...")
        return False


find_item()