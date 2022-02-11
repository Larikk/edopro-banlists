from lib import banlist
from . import lflist

END_DATE = "2010-01-01"

def create():
    banlist.create("generic", lflist.list, enddate=END_DATE)
