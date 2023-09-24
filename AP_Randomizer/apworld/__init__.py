from worlds.AutoWorld import World
from BaseClasses import Region, Location, Item
from .Items import PseudoregaliaItem, PseudoregaliaItemData, item_table, item_frequencies
from .Locations import location_table
from .Regions import region_table
from worlds.generic.Rules import add_rule, set_rule, forbid_item
from .Rules import has_breaker, get_kicks, can_bounce, can_slidejump, can_strikebreak, can_soulcutter, has_small_keys


class PseudoregaliaWorld(World):
    game = "Pseudoregalia"

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}

    def create_item(self, name: str) -> PseudoregaliaItem:
        data = item_table[name]
        return PseudoregaliaItem(name, data.classification, data.code, self.player)

    def create_items(self):
        for item_name, item_data in item_table.items():
            if (item_name == "Dream Breaker"):
                continue  # Really skrunkled way of just adding the one locked breaker to the pool for now.
            if (item_name in item_frequencies):
                for count in range(item_frequencies[item_name]):
                    self.multiworld.itempool.append(
                        Item(item_name, item_data.classification, item_data.code, self.player))
            else:
                self.multiworld.itempool.append(Item(item_name, item_data.classification, item_data.code, self.player))

    def create_regions(self):
        for region_name in region_table.keys():
            self.multiworld.regions.append(Region(region_name, self.player, self.multiworld))

        for loc_name, loc_data in location_table.items():
            region = self.multiworld.get_region(loc_data.region, self.player)
            region.locations.append(Location(self.player, loc_name, loc_data.code, region))

        for region_name, exit_list in region_table.items():
            region = self.multiworld.get_region(region_name, self.player)

            exits = [region_exit.region for region_exit in exit_list]
            region.add_exits(exits, {
                region_exit.region: lambda state, region_exit=region_exit: region_exit.access_rule(state, self.player)
                for region_exit in exit_list
            })

    def set_rules(self):
        self.multiworld.get_location(
            "Dungeon - Dream Breaker",
            self.player).place_locked_item(
            self.create_item("Dream Breaker"))

        # Putting all the access rules here is pretty ugly
        # but I can't be fucked to get it to work properly from another module right now
        set_rule(self.multiworld.get_location("Dungeon - Slide", self.player),
                 lambda state: has_breaker(state, self.player))
        set_rule(self.multiworld.get_location("Keep - Sunsetter", self.player),
                 lambda state: has_breaker(state, self.player))
        set_rule(self.multiworld.get_location("Keep - Strikebreak", self.player), lambda state:
                 (state.has("Slide", self.player) or can_strikebreak(state, self.player))
                 and any([
                     can_slidejump(state, self.player),
                     get_kicks(state, self.player) >= 1,
                     state.has("Cling Gem", self.player)]))
        set_rule(self.multiworld.get_location("Library - Sun Greaves", self.player), lambda state:
                 any([
                     state.has("Slide", self.player) and has_breaker(state, self.player),
                     state.has("Cling Gem", self.player) and has_breaker(state, self.player),
                     # get_kicks(state, self.player) >= 4, Heliacal isn't shuffled yet
                     can_slidejump(state, self.player)]))
        set_rule(self.multiworld.get_location("Theatre - Soul Cutter", self.player), lambda state:
                 can_strikebreak(state, self.player))
        set_rule(self.multiworld.get_location("Bailey - Solar Wind", self.player), lambda state:
                 state.has("Slide", self.player))
        set_rule(self.multiworld.get_location("Underbelly - Ascendant Light", self.player), lambda state:
                 any([
                     can_bounce(state, self.player),
                     get_kicks(state, self.player) >= 3,
                     state.has("Cling Gem", self.player),
                     can_slidejump(state, self.player) and get_kicks(state, self.player) > 0]))
        set_rule(self.multiworld.get_location("Tower - Cling Gem", self.player), lambda state:
                 get_kicks(state, self.player) >= 3)


        set_rule(self.multiworld.get_location("Underbelly - Heliacal Power", self.player), lambda state:
                 has_small_keys(state, self.player) and state.has("Slide", self.player)
                 and any([
                     get_kicks(state, self.player) >= 3,
                     state.has("Sunsetter", self.player)]))
        set_rule(self.multiworld.get_location("Theatre - Aerial Finesse", self.player), lambda state:
                 any([
                     state.has("Cling Gem", self.player) and get_kicks(state, self.player) >= 3,
                     state.has("Cling Gem", self.player) and can_slidejump(state, self.player),
                     can_slidejump(state, self.player) and get_kicks(state, self.player) >= 3]))
        set_rule(self.multiworld.get_location("Castle - Pilgrimage", self.player), lambda state:
                 any([
                     can_bounce(state, self.player),
                     get_kicks(state, self.player) >= 4,
                     state.has("Cling Gem", self.player) and get_kicks(state, self.player) >= 1,
                     state.has_all(["Cling Gem", "Sunsetter"], self.player),
                     state.has("Cling Gem", self.player) and can_slidejump(state, self.player)]))
        set_rule(self.multiworld.get_location("Bailey - Empathy", self.player), lambda state:
                 any([
                     can_slidejump(state, self.player) and state.has("Sunsetter", self.player)
                     and get_kicks(state, self.player) >= 1,
                     can_slidejump(state, self.player) and state.has("Cling Gem", self.player),
                     state.has("Sunsetter", self.player) and get_kicks(state, self.player) >= 3]))
        set_rule(self.multiworld.get_location("Theatre - Empathy", self.player), lambda state:
                 has_small_keys(state, self.player)
                 and state.has("Cling Gem", self.player)
                 and get_kicks(state, self.player) >= 3)
        set_rule(self.multiworld.get_location("Dungeon - Good Graces", self.player), lambda state:
                 state.has("Cling Gem", self.player)
                 or (can_bounce(state, self.player) and get_kicks(state, self.player) >= 3))
        set_rule(self.multiworld.get_location("Castle - Good Graces", self.player), lambda state:
                 state.has("Cling Gem", self.player) and get_kicks(state, self.player) >= 3)
        set_rule(self.multiworld.get_location("Underbelly - Martial Prowess", self.player), lambda state:
                 can_strikebreak(state, self.player) and can_bounce(state, self.player)
                 and any([
                     can_slidejump(state, self.player),
                     get_kicks(state, self.player) >= 1,
                     state.has("Sunsetter", self.player)]))
        set_rule(self.multiworld.get_location("Castle - Clear Mind", self.player), lambda state:
                 state.has("Cling Gem", self.player)
                 or (can_slidejump(state, self.player) and get_kicks(state, self.player) >= 1))
        set_rule(self.multiworld.get_location("Library - Clear Mind", self.player), lambda state:
                 any([
                     can_slidejump(state, self.player),
                     get_kicks(state, self.player) >= 1,
                     state.has("Cling Gem", self.player)]))
        set_rule(self.multiworld.get_location("Keep - Clear Mind", self.player), lambda state:
                 any([
                     state.has("Sunsetter", self.player),
                     state.has("Cling Gem", self.player),
                     get_kicks(state, self.player) >= 1]))
        set_rule(self.multiworld.get_location("Castle - Professionalism", self.player), lambda state:
                 has_small_keys(state, self.player))


        set_rule(self.multiworld.get_location("Bailey - Major Key", self.player), lambda state:
                 any([
                     state.has("Sunsetter", self.player),
                     state.has("Cling Gem", self.player),
                     get_kicks(state, self.player) >= 3]))
        set_rule(self.multiworld.get_location("Underbelly - Major Key", self.player), lambda state:
                 state.has("Sunsetter", self.player)
                 and any([
                     can_soulcutter(state, self.player) and can_bounce(state, self.player),
                     can_slidejump and get_kicks(state, self.player) >= 3,
                     can_soulcutter(state, self.player) and state.has("Cling Gem", self.player)]))
        set_rule(self.multiworld.get_location("Tower - Major Key", self.player), lambda state:
                 state.has("Cling Gem", self.player) and get_kicks(state, self.player) >= 3),
        set_rule(self.multiworld.get_location("Theatre - Major Key", self.player), lambda state:
                 can_soulcutter(state, self.player)
                 and any([
                     state.has("Cling Gem", self.player) and can_slidejump(state, self.player),
                     state.has("Cling Gem", self.player) and get_kicks(state, self.player) > 0]))
        set_rule(self.multiworld.get_location("Keep - Major Key", self.player), lambda state:
                 any([
                     state.has_all(["Cling Gem", "Sunsetter"], self.player)
                     and can_bounce(state, self.player),
                     state.has("Cling Gem", self.player)
                     and can_bounce(state, self.player)
                     and get_kicks(state, self.player) >= 3,
                     state.has_all(["Sunsetter", "Cling Gem"], self.player)
                     and can_bounce(state, self.player)
                     and get_kicks(state, self.player) >= 3]))


        set_rule(self.multiworld.get_location("Dungeon - Small Key On Rafters", self.player), lambda state:
                 any([
                     state.has("Cling Gem", self.player),
                     state.has("Sunsetter", self.player) and get_kicks(state, self.player) >= 3,
                     can_slidejump(state, self.player) and get_kicks(state, self.player) >= 3]))
        set_rule(self.multiworld.get_location("Dungeon - Strong Eyes", self.player), lambda state:
                 has_breaker(state, self.player))
        set_rule(self.multiworld.get_location("Castle - Small Key In Hallway", self.player), lambda state:
                 any([
                     can_slidejump(state, self.player),
                     get_kicks(state, self.player) >= 1,
                     state.has("Sunsetter", self.player),
                     state.has("Cling Gem", self.player)]))
        set_rule(self.multiworld.get_location("Castle - High Small Key", self.player), lambda state:
                 state.has("Cling Gem", self.player) or get_kicks(state, self.player) >= 3)
        set_rule(self.multiworld.get_location("Keep - Small Key", self.player), lambda state:
                 has_breaker(state, self.player))
        set_rule(self.multiworld.get_location("Bailey - Small Key", self.player), lambda state:
                 state.has("Slide", self.player))
        set_rule(self.multiworld.get_location("Underbelly - Small Key", self.player), lambda state:
                 state.has("Sunsetter", self.player) or can_slidejump(state, self.player))


        # TODO: Replace with a proper event
        self.multiworld.completion_condition[self.player] = lambda state: state.has_all([
            "Major Key - Empty Bailey",
            "Major Key - The Underbelly",
            "Major Key - Tower Remains",
            "Major Key - Sansa Keep",
            "Major Key - Twilight Theatre",
        ], self.player) and self.multiworld.get_region("The Great Door", self.player).can_reach(state)
