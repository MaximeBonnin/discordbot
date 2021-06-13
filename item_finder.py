import requests
from bs4 import BeautifulSoup


def find_img(item):  # checks other site for img
    try:
        URL = f'https://www.aidedd.org/dnd/om.php?vo={item}'
        site = requests.get(URL)
        soup = BeautifulSoup(site.content, 'html.parser')
        content = soup.find(class_='bloc')
        img_found = content.find(class_="picture").find("amp-img")["src"]
        return img_found

    except AttributeError:
        print("No image found.")
        return False


def find_item_easy(term):  # checks main source for item info
    item_type, item = term.split(":")
    if item_type == "item":
        item_type = "wondrous-items"
    url2 = f"http://dnd5e.wikidot.com/{item_type}:{item}"

    site = requests.get(url2)
    soup = BeautifulSoup(site.content, 'html.parser')
    content = soup.find(id="page-content")

    x = content
    output = ""
    while x.find_next().text != "":
        if x.find_next().text.strip("\n") not in output:
            y = x.find_next().text.strip("\n")
            output = output + y + "\n"

        x = x.find_next()

    if f"The page {term} you want to access does not exist." in output:
        print("Not found.")
        return False
    else:
        title = ""   # format title
        for i in item.split("-"):
            title = title + i.capitalize() + " "

        if find_img(item):   # attach img to top of output if one exists
            output = f"{find_img(item)}\n{output}"
        output = f"**{title}:**\n{output}"  # attach title to top of output

    if len(output) > 2000:  # make output fit for discord character limit
        msg = []
        for i in range(0, len(output), 2000):
            line = output[i:i+2000]
            msg.append(line)
        return msg
    return [output]
