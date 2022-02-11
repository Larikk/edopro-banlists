from enum import Enum
import os
import requests
from . import cardutil
from . import unofficialcards
from . import namecondition
from . import fileutil


class CardGroup(Enum):
    FORBIDDEN = 1
    LIMITED = 2
    SEMILIMITED = 3
    UNLIMITED = 4


cardLimits = {
    CardGroup.FORBIDDEN: 0,
    CardGroup.LIMITED: 1,
    CardGroup.SEMILIMITED: 2,
    CardGroup.UNLIMITED: 3,
}


def formatCard(card, n):
    return f"{card['id']} {n}".ljust(20) + f"-- {card['name']}\n"


def getIds(groups):
    ids = set()
    for group, cards in groups.items():
        for card in cards:
            ids.add(card["id"])
    return ids


def createLfRegion(lfgroups):
    s = ""

    for cardGroup, cards in lfgroups.items():
        if len(cards) > 0:
            n = cardLimits[cardGroup]
            s += "#" + str(cardGroup.name) + "\n"
            s += "".join([formatCard(card, n) for card in cards])

    return s


def createNameConditionRegion(ids):
    illegalCards = []

    for card in namecondition.cards:
        id = card["id"]
        alias = card["alias"]
        if alias in ids and id not in ids:
            illegalCards.append(card)

    s = ""

    def func(c): return formatCard(c, -1)

    if len(illegalCards) > 0:
        s += "# Block cards that are always treated as another name and should not be legal\n"
        s += "".join([func(card) for card in illegalCards])

    return s


def createUnofficialCardRegion(lfgroups, ids):
    sectionsOfUnofficialCards = unofficialcards.find(ids)

    idLimitMapping = dict()

    for group, cards in lfgroups.items():
        n = cardLimits[group]
        for card in cards:
            idLimitMapping[card["id"]] = n

    def preerrateFunc(c): return formatCard(c, idLimitMapping[c["alias"]])
    def illegalFunc(c): return formatCard(c, -1)

    s = ""

    for section in sectionsOfUnofficialCards:
        s += "#" + section["name"] + "\n"
        preerrataCards = section["preerrata"]
        illegalCards = section["illegal"]
        s += "".join([preerrateFunc(card) for card in preerrataCards])
        s += "".join([illegalFunc(card) for card in illegalCards])

    return s


def encodeList(name, lfgroups):
    ids = getIds(lfgroups)

    s = f"#[{name}]\n!{name}\n$whitelist\n"

    s += createLfRegion(lfgroups)
    s += createNameConditionRegion(ids)
    s += createUnofficialCardRegion(lfgroups, ids)

    return s


def determineBanGroup(id, lflist):
    if id in lflist["forbidden"]:
        return CardGroup.FORBIDDEN
    elif id in lflist["limited"]:
        return CardGroup.LIMITED
    elif id in lflist["semilimited"]:
        return CardGroup.SEMILIMITED
    else:
        return CardGroup.UNLIMITED


def groupCardsByLfStatus(cards, lfType):
    groups = {
        CardGroup.FORBIDDEN: [],
        CardGroup.LIMITED: [],
        CardGroup.SEMILIMITED: [],
        CardGroup.UNLIMITED: [],
    }

    for card in cards:
        # The id sometimes points to an alt artwork
        card["id"] = cardutil.findMainId(card)
        group = determineBanGroup(card["id"], lfType)
        groups[group].append(card)

    return groups


def filterByDate(cards, start, end):
    if start is None:
        start = "2000-01-01"

    if end is None:
        end = "2050-01-01"

    def f(card):
        r = cardutil.findReleaseDate(card)
        if r is None:
            return False
        else:
            return r >= start and r <= end

    return filter(lambda c: f(c), cards)


def create(name, lflist, outdir="", cardfilter=None, startdate=None, enddate=None):
    url = "https://db.ygoprodeck.com/api/v7/cardinfo.php?misc=yes"
    cards = fileutil.load(url, "cardinfo")["data"]

    if startdate is not None or enddate is not None:
        cards = filterByDate(cards, startdate, enddate)

    if cardfilter is not None:
        cards = filter(cardfilter, cards)

    cards = list(cards)

    lfgroups = groupCardsByLfStatus(cards, lflist)
    filecontent = encodeList(name, lfgroups)

    filename = name + ".conf"

    outdir = ("lists/" + outdir).rstrip("/") + "/"
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    with open(outdir + filename, "w") as f:
        f.write(filecontent)
