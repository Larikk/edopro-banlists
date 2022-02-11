import sqlite3
import os

DB_DIR = "CDB/"

def hasUnofficialCards(db):
    keywords = {
        "unofficial",
        "goat",
        "deckmaster",
        "skills",
        "rush",
        "remove",
    }

    for keyword in keywords:
        if keyword in db:
            return True
    return False


def find(ids):
    officialIds = set(ids)

    databases = os.listdir(DB_DIR)
    databases = filter(lambda f: f.endswith(".cdb"), databases)
    databases = filter(lambda f: hasUnofficialCards(f), databases)

    sectionsWithUnofficialCards = []

    for db in databases:
        dbPath = DB_DIR + db
        with sqlite3.connect(dbPath) as con:
            preerrataCards = []
            illegalCards = []
            cursor = con.cursor()
            sql = """SELECT datas.id, datas.alias, texts.name FROM datas INNER JOIN texts ON datas.id = texts.id WHERE datas.alias != 0 ORDER BY texts.name"""
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                id = row[0]
                alias = row[1]
                name = row[2].strip()

                if alias in officialIds:
                    card = {"id": id, "name": name, "alias": alias}
                    if "(Pre-Errata)" in name:
                        preerrataCards.append(card)
                    else:
                        illegalCards.append(card)

            if len(illegalCards) + len(preerrataCards) > 0:
                sectionsWithUnofficialCards.append({"name": db, "illegal": illegalCards, "preerrata": preerrataCards})

    return sectionsWithUnofficialCards
