import sys
import formats.generic.lflistcreator as generic
import formats.juniorjourney.lflistcreator as juniorjourney
import formats.abyssrising.lflistcreator as abyssrising

mappings = {
    "generic": generic,
    "junior-journey": juniorjourney,
    "abyss-rising": abyssrising,
}

if len(sys.argv) < 2:
    print("Usage: python main.py <format>")
    exit(1)

format = sys.argv[1]
format = format.lower()

if format not in mappings:
    print("Invalid format. Supported formats are:\n" + "\n".join([format for format, _ in mappings.items()]))

mappings[format].create()
