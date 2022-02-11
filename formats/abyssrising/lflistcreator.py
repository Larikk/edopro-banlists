from urllib import request
from lib import banlist
from . import lflist
import requests
import os

END_DATE = "2012-11-20"

def initReleaseDateMap():
    url = "https://db.ygoprodeck.com/api/v7/cardsets.php"
    releases = requests.get(url).json()

    mapping = dict()

    for release in releases:
        if "tcg_date" in release:
            mapping[release["set_name"].lower()] = release["tcg_date"]

    return mapping

# Function returns whether a card had a release before before END_DATE that is not from a Duel terminal
def isCardLegal(card, releaseDateMapping):
    if "card_sets" not in card:
        return False

    # Loop tries to find the lowest release date that is not from a Duel Terminal
    firstReleaseDate = "2100-01-01"
    for release in card["card_sets"]:
        name = release["set_name"].lower()

        if "duel terminal" in name:
            # Ignore this release
            continue

        if name not in releaseDateMapping:
            # Ignore releases that are not in the card sets endpoint
            print("Unknown release " + name)
            continue

        date = releaseDateMapping[name]
        firstReleaseDate = min(date, firstReleaseDate)
    
    if firstReleaseDate > END_DATE:
        print("Removing card " + card["name"])

    return firstReleaseDate <= END_DATE

def create():
    releaseDateMapping = initReleaseDateMap()
    banlist.create("abyss-rising", lflist.list, cardfilter=lambda c: isCardLegal(c, releaseDateMapping), enddate=END_DATE)
