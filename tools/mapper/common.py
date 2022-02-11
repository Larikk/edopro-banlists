import requests

def findMainId(card):
    if card['name'] == "Dark Magician":
        return 46986414

    ids = map(lambda e: e['id'], card['card_images'])
    mainId = min(ids)
    return mainId

def mapNamesToIds(names):
    url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
    params = {
        "format": "tcg",
        "name": "|".join(sorted(names)),
        "misc": "yes",
    }

    response = requests.get(url, params=params)

    if not response.ok:
        print("Request failed")
        print(response.body)
        exit(1)

    cards = response.json()["data"]
    mapping = dict()

    for card in cards:
        name = card['name'].lower()
        id = findMainId(card)
        mapping[name] = id

        # Handle name changes
        for miscEntry in card['misc_info']:
            if 'beta_name' in miscEntry:
                betaName = miscEntry['beta_name'].lower()
                mapping[betaName] = id

    successful = True
    for name in names:
        if name.lower() not in mapping:
            print("Not found: " + name)
            successful = False
    
    if not successful:
        exit(1)

    return mapping
