from BaseClasses import Location
from typing import NamedTuple, Dict, Optional


class PseudoregaliaLocationData(NamedTuple):
    region: str
    code: int = None
    locked_item: Optional[str] = None
    show_in_spoiler: bool = True


location_table = {
    # Sorted by greater region, then subregion
    # Then abilities and major keys first
    # Then alphabetically

    "Dungeon - Dream Breaker": PseudoregaliaLocationData(
        # Dream Breaker can't really be shuffled right now but I would like to later
        code=2365810001,
        region="Dungeon Mirror",
        locked_item="Dream Breaker"),
    "Dungeon - Slide": PseudoregaliaLocationData(
        code=2365810002,
        region="Dungeon Mirror"),
    "Dungeon - Alcove Near Mirror": PseudoregaliaLocationData(
        code=2365810030,
        region="Dungeon Mirror",),
    "Dungeon - Dark Orbs": PseudoregaliaLocationData(
        code=2365810016,
        region="Dungeon Mirror",),
    "Dungeon - Past Poles": PseudoregaliaLocationData(
        code=2365810031,
        region="Dungeon Strong Eyes",),
    "Dungeon - Rafters": PseudoregaliaLocationData(
        code=2365810023,
        region="Dungeon Strong Eyes",),
    "Dungeon - Strong Eyes": PseudoregaliaLocationData(
        code=2365810024,
        region="Dungeon Strong Eyes",),

    "Castle - Indignation": PseudoregaliaLocationData(
        code=2365810003,
        region="Castle Main"),
    "Castle - Alcove Near Dungeon": PseudoregaliaLocationData(
        code=2365810032,
        region="Castle Main",),
    "Castle - Balcony": PseudoregaliaLocationData(
        code=2365810036,
        region="Castle Main",),
    "Castle - Corner Corridor": PseudoregaliaLocationData(
        code=2365810033,
        region="Castle Main",),
    "Castle - Floater In Courtyard": PseudoregaliaLocationData(
        code=2365810013,
        region="Castle Main",),
    "Castle - Locked Door": PseudoregaliaLocationData(
        code=2365810022,
        region="Castle Main",),
    "Castle - Platform In Main Halls": PseudoregaliaLocationData(
        code=2365810025,
        region="Castle Main",),
    "Castle - Tall Room Near Wheel Crawlers": PseudoregaliaLocationData(
        code=2365810026,
        region="Castle Main",),
    "Castle - Wheel Crawlers": PseudoregaliaLocationData(
        code=2365810034,
        region="Castle Main",),
    "Castle - High Climb From Courtyard": PseudoregaliaLocationData(
        code=2365810019,
        region="Castle High Climb",),
    "Castle - Alcove Near Scythe Corridor": PseudoregaliaLocationData(
        code=2365810035,
        region="Castle By Scythe Corridor",),
    "Castle - Near Theatre Front": PseudoregaliaLocationData(
        code=2365810017,
        region="Castle Moon Room",),

    "Keep - Strikebreak": PseudoregaliaLocationData(
        code=2365810005,
        region="Keep Main"),
    "Keep - Major Key": PseudoregaliaLocationData(
        code=2365810049,
        region="Keep Main",),
    "Keep - Alcove Near Locked Door": PseudoregaliaLocationData(
        code=2365810039,
        region="Keep Main",),
    "Keep - Levers Room": PseudoregaliaLocationData(
        code=2365810027,
        region="Keep Main",),
    "Keep - Near Theatre": PseudoregaliaLocationData(
        code=2365810021,
        region="Keep Main",),
    "Keep - Sunsetter": PseudoregaliaLocationData(
        code=2365810004,
        region="Keep Sunsetter"),

    "Library - Sun Greaves": PseudoregaliaLocationData(
        code=2365810006,
        region="Library Main"),
    "Library - Upper Back": PseudoregaliaLocationData(
        code=2365810037,
        region="Library Main",),
    "Library - Locked Door Across": PseudoregaliaLocationData(
        code=2365810020,
        region="Library Locked",),
    "Library - Locked Door Left": PseudoregaliaLocationData(
        code=2365810038,
        region="Library Locked",),

    "Theatre - Soul Cutter": PseudoregaliaLocationData(
        code=2365810007,
        region="Theatre Main"),
    "Theatre - Major Key": PseudoregaliaLocationData(
        code=2365810050,
        region="Theatre Main",),
    "Theatre - Back Of Auditorium": PseudoregaliaLocationData(
        code=2365810045,
        region="Theatre Main",),
    "Theatre - Locked Door": PseudoregaliaLocationData(
        code=2365810015,
        region="Theatre Main",),
    "Theatre - Murderous Goat": PseudoregaliaLocationData(
        code=2365810044,
        region="Theatre Main",),
    "Theatre - Corner Beam": PseudoregaliaLocationData(
        code=2365810012,
        region="Theatre Pillar",),

    "Bailey - Solar Wind": PseudoregaliaLocationData(
        code=2365810008,
        region="Empty Bailey"),
    "Bailey - Center Steeple": PseudoregaliaLocationData(
        code=2365810040,
        region="Empty Bailey",),
    "Bailey - Cheese Bell": PseudoregaliaLocationData(
        code=2365810014,
        region="Empty Bailey",),
    "Bailey - Inside Building": PseudoregaliaLocationData(
        code=2365810028,
        region="Empty Bailey",),

    "Underbelly - Ascendant Light": PseudoregaliaLocationData(
        code=2365810009,
        region="Underbelly Main"),
    "Underbelly - Alcove Near Light": PseudoregaliaLocationData(
        code=2365810043,
        region="Underbelly Main",),
    "Underbelly - Building Near Little Guy": PseudoregaliaLocationData(
        code=2365810042,
        region="Underbelly Main",),
    "Underbelly - Locked Door": PseudoregaliaLocationData(
        code=2365810011,
        region="Underbelly Main",),
    "Underbelly - Main Room": PseudoregaliaLocationData(
        code=2365810029,
        region="Underbelly Main",),
    "Underbelly - Rafters Near Keep": PseudoregaliaLocationData(
        code=2365810041,
        region="Underbelly Hole",),
    "Underbelly - Strikebreak Wall": PseudoregaliaLocationData(
        code=2365810018,
        region="Underbelly Main",),
    "Underbelly - Major Key": PseudoregaliaLocationData(
        code=2365810047,
        region="Underbelly Hole",),

    "Tower - Cling Gem": PseudoregaliaLocationData(
        code=2365810010,
        region="Tower Remains"),
    "Tower - Major Key": PseudoregaliaLocationData(
        code=2365810048,
        region="The Great Door",),

    "Dungeon - Unlock Door": PseudoregaliaLocationData(
        region="Dungeon Strong Eyes",
        locked_item="Unlocked Door",
        show_in_spoiler=False),
    "Castle - Unlock Door (Professionalism)": PseudoregaliaLocationData(
        region="Castle Main",
        locked_item="Unlocked Door",
        show_in_spoiler=False),
    "Castle - Unlock Door (Sansa Keep)": PseudoregaliaLocationData(
        region="Castle Main",
        locked_item="Unlocked Door",
        show_in_spoiler=False),
    "Keep - Unlock Door": PseudoregaliaLocationData(
        region="Keep Main",
        locked_item="Unlocked Door",
        show_in_spoiler=False),
    "Library - Unlock Door": PseudoregaliaLocationData(
        region="Library Main",
        locked_item="Unlocked Door",
        show_in_spoiler=False),
    "Theatre - Unlock Door": PseudoregaliaLocationData(
        region="Theatre Main",
        locked_item="Unlocked Door",
        show_in_spoiler=False),
    "Underbelly - Unlock Door": PseudoregaliaLocationData(
        region="Underbelly Main",
        locked_item="Unlocked Door",
        show_in_spoiler=False),

    "D S T RT ED M M O   Y": PseudoregaliaLocationData(
        region="The Great Door",
        locked_item="Something Worth Being Awake For"),
}
