def findMainId(card):
    # Alt artworks have in general the same id as the main artwork
    # There are two exceptions though: Dark Magician and Polymerization

    # YGOPRODECK assigns alt artworks their own ids
    # They start with the main id and increment upwards by one
    # To get the main id we just need to find the lowest id in 'card_images'

    # This works fine for all regular cards and Polymerization
    # The DM alt artwork has a lower id than the main artwork
    # Therefore we need to handle that separately
    if card['name'] == "Dark Magician":
        return 46986414

    def f(e): return e['id']
    ids = map(f, card['card_images'])
    mainId = min(ids)
    return mainId

def findReleaseDate(card):
    releaseDate = None
    for entry in card["misc_info"]:
        if "tcg_date" in entry:
            if releaseDate is None:
                releaseDate = entry["tcg_date"]
            else:
                releaseDate = min(entry["tcg_date"], releaseDate)

    return releaseDate
