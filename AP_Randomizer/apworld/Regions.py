from typing import NamedTuple, Callable, Dict, List, Optional
from BaseClasses import CollectionState
from Rules import has_breaker, can_bounce, get_kicks, has_small_keys, navigate_darkrooms, can_slidejump


class RegionExit(NamedTuple):
    region: str
    access_rule: Callable[[CollectionState, int], bool] = lambda state, player: True
    breakable_wall: bool = False


region_table: Dict[str, List[RegionExit]] = {
    "Menu": [RegionExit("Dungeon Mirror")],
    "Dungeon Mirror": [RegionExit("Dungeon Strong Eyes",
                                  lambda state, player: state.has("Slide", player)),
                       RegionExit("Underbelly Main", has_breaker),
                       RegionExit("Theatre Main",
                                  lambda state, player:
                                  any(
                                      get_kicks >= 3,
                                      state.has("Cling Gem"),
                                      can_slidejump and get_kicks >= 1,
                                      can_bounce,
                                  )
                                  )],
    "Dungeon Strong Eyes": [RegionExit("Castle Sansa", has_small_keys)],
    "Castle Sansa": [RegionExit("Library Main", has_breaker),
                     RegionExit("Keep Main"),
                     RegionExit("Empty Bailey"),
                     RegionExit("Theatre Pillar",
                                lambda state, player:
                                any(
                                    get_kicks(state, player) > 0,
                                    state.has("Cling Gem", player),
                                    state.has("Sunsetter", player),
                                )),
                     RegionExit("Theatre Main",
                                lambda state, player:
                                any(
                                    state.has("Cling Gem", player),
                                    can_slidejump and get_kicks >= 4,
                                ))],
    "Library Main": [RegionExit("Library Locked", has_small_keys)],
    "Library Locked": [],  # There's no point in connecting this back to library main.
    "Keep Main": [RegionExit("Keep Sunsetter",
                             lambda state, player:
                             any(
                                 has_small_keys(state, player),
                                 state.has("Cling Gem", player),
                                 get_kicks(state, player) >= 3,
                             )),
                  RegionExit("Underbelly Hole",
                             lambda state, player:
                             any(
                                 get_kicks(state, player) > 0,
                                 state.has("Sunsetter", player),
                             )),
                  RegionExit("Theatre Main",
                             lambda state, player:
                             any(
                                 state.has("Cling Gem") and get_kicks >= 3,
                                 state.has("Cling Gem") and can_slidejump,
                             ))],
    "Keep Sunsetter": [],
    "Empty Bailey": [RegionExit("Castle Sansa"),
                     RegionExit("Tower Remains",
                                lambda state, player:
                                any(
                                    get_kicks(state, player) > 0,
                                    state.has("Cling Gem", player),
                                    state.has_all(["Slide", "Sunsetter"], player)
                                )),
                     RegionExit("Theatre Pillar")],
    "Tower Remains": [RegionExit("Underbelly Main",  # Simplified access rule copied from spuds' logic.
                                 lambda state, player: state.has("Sunsetter", player)),
                      RegionExit("The Great Door",
                                 lambda state, player:
                                 state.has("Cling Gem") and get_kicks >= 3)],
    "Underbelly Main": [RegionExit("Empty Bailey")],
    "Underbelly Hole": [RegionExit("Underbelly Main",
                                   lambda state, player: state.has("Sunsetter", player))],  # I don't actually know what this is.
    "Theatre Main": [RegionExit("Keep Main",
                                lambda state, player: state.has("Cling Gem", player))],
    "Theatre Pillar": [RegionExit("Theatre Main",
                                  lambda state, player:
                                  any(
                                      state.has_all(["Sunsetter", "Cling Gem"], player),
                                      state.has("Sunsetter", player) and get_kicks >= 4,
                                  ))],
    "The Great Door": [],
}
