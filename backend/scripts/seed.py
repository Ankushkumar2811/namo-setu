"""Deterministic development seed data with no production credentials or personal data."""

from itertools import cycle
from random import Random

TEMPLE_NAMES = [
    "Kashi Vishwanath", "Kedarnath Dham", "Mahakaleshwar", "Jagannath Temple",
    "Somnath", "Mallikarjuna", "Mahakali Shakti Peeth", "Omkareshwar",
    "Baidyanath Dham", "Rameshwaram", "Nageshwar", "Trimbakeshwar",
    "Bhimashankar", "Grishneshwar", "Badrinath", "Dwarkadhish",
    "Kamakhya", "Meenakshi Amman", "Brihadeeswarar", "Vaishno Devi",
]
PLACES = [
    ("Varanasi", "Uttar Pradesh", 25.3109, 83.0107),
    ("Ujjain", "Madhya Pradesh", 23.1765, 75.7885),
    ("Puri", "Odisha", 19.8048, 85.8178),
    ("Haridwar", "Uttarakhand", 29.9457, 78.1642),
    ("Nashik", "Maharashtra", 19.9975, 73.7898),
    ("Madurai", "Tamil Nadu", 9.9252, 78.1198),
    ("Guwahati", "Assam", 26.1445, 91.7362),
    ("Jammu", "Jammu and Kashmir", 32.7266, 74.8570),
]


def build_seed() -> dict[str, list[dict[str, object]]]:
    rng = Random(108)
    places = cycle(PLACES)
    temples: list[dict[str, object]] = []
    for index in range(120):
        base = TEMPLE_NAMES[index % len(TEMPLE_NAMES)]
        city, state, latitude, longitude = next(places)
        name = base if index < len(TEMPLE_NAMES) else f"{base} Heritage Shrine {index + 1}"
        temples.append({
            "name": name,
            "slug": name.casefold().replace(" ", "-"),
            "city": city,
            "state": state,
            "category": ["Jyotirlinga", "Shakti Peetha", "Char Dham", "Heritage"][index % 4],
            "latitude": round(latitude + rng.uniform(-0.05, 0.05), 6),
            "longitude": round(longitude + rng.uniform(-0.05, 0.05), 6),
            "rating": round(rng.uniform(4.0, 4.9), 1),
            "is_verified": index < 40,
        })
    hotels = [
        {"name": f"{city} Pilgrim Residency {index + 1}", "city": city, "rooms": 20 + index % 35}
        for index, (city, _, _, _) in zip(range(50), cycle(PLACES), strict=False)
    ]
    dharamshalas = [
        {"name": f"{city} Seva Sadan {index + 1}", "city": city, "beds": 30 + index % 70}
        for index, (city, _, _, _) in zip(range(25), cycle(PLACES), strict=False)
    ]
    guides = [
        {"full_name": f"Verified Guide {index + 1}", "languages": ["Hindi", "English"], "experience_years": 2 + index % 18}
        for index in range(100)
    ]
    pandits = [
        {"full_name": f"Verified Pandit {index + 1}", "languages": ["Hindi", "Sanskrit"], "experience_years": 3 + index % 25}
        for index in range(100)
    ]
    return {"temples": temples, "hotels": hotels, "dharamshalas": dharamshalas, "guides": guides, "pandits": pandits}


if __name__ == "__main__":
    import json
    print(json.dumps(build_seed(), ensure_ascii=False, indent=2))
