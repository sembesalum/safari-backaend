"""Seed transfer service content copied from frontend Transfers page."""

from __future__ import annotations

from typing import Any


TRANSFER_SEED_DATA: list[dict[str, Any]] = [
    {
        "title": "Airport & hotel transfers",
        "segment": "airport",
        "summary": "All major routes: Airport-Stone Town, east coast, north coast, and cross-island. Per vehicle pricing by group size.",
        "description": "Travel around Zanzibar safely, comfortably, and on time with clean, air-conditioned vehicles and experienced local drivers.",
        "from_price": "From $30 / vehicle (1-6 people)",
        "status": "active",
        "pricing_payload": {
            "airport_routes": [
                {
                    "id": "airport-stone-town",
                    "title": "Airport -> Stone Town",
                    "subtitle": "Capital city of the island",
                    "rows": [
                        {"group": "1-6 people", "price": "$30 per vehicle"},
                        {"group": "7-14 people", "price": "$35 per vehicle"},
                        {"group": "15-28 people", "price": "$45 per vehicle"},
                    ],
                },
                {
                    "id": "airport-paje-jambiani",
                    "title": "Airport / Stone Town -> Paje / Jambiani",
                    "subtitle": "East coast of Zanzibar",
                    "rows": [
                        {"group": "1-6 people", "price": "$50 per vehicle"},
                        {"group": "7-14 people", "price": "$70 per vehicle"},
                        {"group": "15-28 people", "price": "$110 per vehicle"},
                    ],
                },
                {
                    "id": "airport-nungwi-kendwa",
                    "title": "Airport / Stone Town -> Nungwi / Kendwa",
                    "subtitle": "North coast beaches",
                    "rows": [
                        {"group": "1-6 people", "price": "$50 per vehicle"},
                        {"group": "7-14 people", "price": "$70 per vehicle"},
                        {"group": "15-28 people", "price": "$110 per vehicle"},
                    ],
                },
                {
                    "id": "airport-matemwe-kiwengwa",
                    "title": "Airport / Stone Town -> Matemwe / Kiwengwa",
                    "subtitle": "Near the north beach side",
                    "rows": [
                        {"group": "1-6 people", "price": "$45 per vehicle"},
                        {"group": "7-14 people", "price": "$65 per vehicle"},
                        {"group": "15-28 people", "price": "$100 per vehicle"},
                    ],
                },
                {
                    "id": "paje-jambiani-nungwi-kendwa",
                    "title": "Paje / Jambiani -> Nungwi / Kendwa",
                    "subtitle": "East coast to north coast",
                    "rows": [
                        {"group": "1-6 people", "price": "$55 per vehicle"},
                        {"group": "7-14 people", "price": "$75 per vehicle"},
                        {"group": "15-28 people", "price": "$115 per vehicle"},
                    ],
                },
            ]
        },
    },
    {
        "title": "Half day tour transfer",
        "segment": "half_day",
        "summary": "Private half-day transfer with driver and flexible itinerary. Extra hour available.",
        "description": "Comfortable and reliable half day transport, ideal for visiting popular Zanzibar attractions.",
        "from_price": "$70 / vehicle (1-6 people)",
        "status": "active",
        "pricing_payload": {
            "half_day_tiers": [
                {"group": "1-6 people", "price": "$70 per vehicle"},
                {"group": "7-14 people", "price": "$165 per vehicle"},
                {"group": "15-28 people", "price": "$220 per vehicle"},
            ],
            "extra_hour": "$20 per hour",
            "includes": [
                "Private vehicle",
                "Professional driver",
                "Fuel costs",
                "Waiting time during tour",
                "Parking fees",
            ],
            "excludes": ["Entrance fees", "Tour guide fees", "Boat fees", "Personal expenses"],
            "recommended_stops": [
                "Stone Town street walks",
                "Spice farm",
                "Jozani monkey forest",
                "Prison Island",
                "Local village tour",
                "Shopping and souvenirs",
            ],
        },
    },
    {
        "title": "Full day tour transfer (12 hours)",
        "segment": "full_day",
        "summary": "Flexible full-day private transfer for multi-stop routes, sightseeing, and custom itineraries.",
        "description": "Your driver stays with you all day so you can explore at your own pace around Zanzibar.",
        "from_price": "$85 / vehicle (1-6 people)",
        "status": "active",
        "pricing_payload": {
            "full_day_tiers": [
                {"group": "1-6 people", "price": "$85 per vehicle"},
                {"group": "7-14 people", "price": "$220 per vehicle"},
                {"group": "15-28 people", "price": "$320 per vehicle"},
            ],
            "extra_hour": "$20 per hour",
            "includes": [
                "Private vehicle",
                "Professional driver",
                "Fuel costs",
                "Waiting time during tour",
                "Parking fees",
                "Flexible stops",
            ],
            "excludes": ["Entrance fees", "Tour guide fees", "Boat fees", "Personal expenses", "Meals and drinks"],
            "recommended_destinations": [
                "Stone Town street walks",
                "Spice farm",
                "Jozani monkey forest",
                "Prison Island",
                "Local village tour",
                "Shopping and souvenirs",
            ],
            "use_cases": [
                "Island sightseeing tours",
                "Visiting multiple attractions",
                "Beach hopping",
                "Cultural and historical tours",
                "Shopping and restaurant visits",
                "Customized private tours",
            ],
        },
    },
]
