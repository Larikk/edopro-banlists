from lib import banlist
from . import lflist

def createCompleteList(year):
    year = str(year)
    name = "jj-format-" + year
    enddate = year + "-12-31"

    banlist.create(name, lflist.list, outdir="junior-journey", enddate=enddate)

def createYearlyReleaseList(year):
    year = str(year)
    name = "jj-releases-" + year
    startdate = year + "-01-01"
    enddate = year + "-12-31"

    emptylflist = {
        "forbidden": {},
        "limited": {},
        "semilimited": {},
    }

    banlist.create(name, emptylflist, outdir="junior-journey", startdate=startdate, enddate=enddate)



def create():
    createCompleteList(2005)

    for i in range(2005, 2008):
       createYearlyReleaseList(i)