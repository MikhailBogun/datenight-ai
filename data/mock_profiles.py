"""Mock Instagram profile dumps keyed by username."""

PROFILES: dict[str, str] = {
    "@art_girl": """
BIO: 🎨 painter & gallery hopper | coffee snob ☕ | lost in museums
     florence was a dream 🇮🇹 | she/her | DMs open for collabs

RECENT POSTS:
- "just finished this oil painting, three weeks of work 🖼️ #oilpainting #fineart"
- "Sunday at the Tate — Hockney never gets old 😭 #artlover #london"
- "obsessed with this documentary about Basquiat. street art changed everything"
- "slow mornings, good books, and decent espresso ✨ #bookstagram"
- "film photography >>> digital, unpopular opinion but I stand by it 📷"
- "re-reading Donna Tartt's The Secret History for the 4th time 📖"

HASHTAGS USED: #fineart #oilpainting #bookstagram #filmphotography #museums
               #aestheticlife #arthistory #slowliving #vintagefinds #italianart
""",

    "@tech_babe": """
BIO: 🚀 software dev by day | sci-fi nerd by night | she/her
     building things that matter | coffee-powered ☕ | Berlin 🇩🇪

RECENT POSTS:
- "just deployed my first Rust project. painful but worth it 💻 #rustlang"
- "Black Mirror season 7 thoughts: disturbing as always but can't stop watching"
- "weekend hackathon w/ the team — we shipped something wild 🔥 #buildinpublic"
- "reading Asimov's Foundation series for the second time. still blows my mind"
- "cyberpunk aesthetics IRL — Tokyo street photography dump 🌆 #cyberpunk"
- "ngl Blade Runner 2049 is a perfect film. fight me. #scifi #movies"

HASHTAGS USED: #scifi #programming #rustlang #techgirl #cyberpunk #asimov
               #blackmirror #buildinpublic #dystopia #futuretech
""",

    "@sport_girl": """
BIO: 🏃‍♀️ marathon runner | yoga instructor | plant-based 🌱
     chasing endorphins & sunrises | outdoor adventures | she/her

RECENT POSTS:
- "5am run before the city wakes up. nothing beats it 🌅 #running #morningrun"
- "just finished a 10-day silent meditation retreat. life-changing 🧘"
- "plant-based meal prep Sunday 🥗 #veganfood #mealprep"
- "documentary rec: 'Free Solo' — Alex Honnold is not human #climbing #documentary"
- "yoga flow on the rooftop at sunset 🌇 #yoga #yogalife"
- "reading 'Born to Run' again. every runner needs this book 📚 #ultramarathon"

HASHTAGS USED: #running #yoga #plantbased #meditation #outdoorlife #marathon
               #vegan #freeSolo #climbing #wellness
""",

    "@fashion_muse": """
BIO: 👗 vintage collector | thrift queen 👑 | Paris 🥐 twice a year
     sustainable fashion advocate | she/her | collabs: DM me

RECENT POSTS:
- "found a 1970s Yves Saint Laurent blazer for €12. I am unstoppable 🔥 #thrifting"
- "Paris Fashon Week street style dump — people are ART out there 📸"
- "rewatching Emily in Paris for the outfits only, zero shame #emilyinparis"
- "Coco Chanel documentary on Netflix is SO good — highly recommend"
- "romanticize your life aesthetic 🌹 #slowliving #romanticizelife"
- "sustainable fashion swap event this Saturday! #sustainablefashion"

HASHTAGS USED: #vintage #thrifting #sustainablefashion #parisfashion #ootd
               #slowfashion #aestheticlife #fashionhistory #frenchgirl #romanticizelife
""",
}


def get_profile(username: str) -> str | None:
    return PROFILES.get(username.lower())


AVAILABLE_USERNAMES = list(PROFILES.keys())
