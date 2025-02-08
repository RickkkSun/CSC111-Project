"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from __future__ import annotations
import json
from typing import Optional

from game_entities import Location, Item, NPC, Player
from proj1_event_logger import Event, EventList


# Note: You may add in other import statements here as needed

# Note: You may add helper functions, classes, etc. below as needed


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - current_location_id: the id of the current location the player is in.
        - ongoing: whether the game is ongoing.
        - inventory: a list of items currently held by the player.
        - score: the player's current score.
        - moves_made: the total number of moves made by the player.
        - moves_limit: the maximum number of moves allowed before the game ends.
        - npcs: a list of non-player characters in the game.
        - player: an instance of the Player class representing the player.

    Representation Invariants:
        - current_location_id in self._locations
        - moves_made >= 0 and moves_made <= moves_limit
        - score >= 0
        - player.score == score
        - player.current_location == current_location_id
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: list[Item]
    player: Player
    npcs: list[NPC]
    moves_made: int
    move_limit: int
    ongoing: bool

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        # NOTES:
        # You may add parameters/attributes/methods to this class as you see fit.

        # Requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

        # Suggested helper method (you can remove and load these differently if you wish to do so):
        self.player = Player(initial_location_id, [], 500, 0)
        self._locations, self._items = self._load_game_data(game_data_file)
        self.npcs = self._load_npcs(game_data_file)
        self.moves_made = 0
        self.move_limit = 20
        self.ongoing = True
        self.game_log = game_log

        start_event = Event(self.player.current_location, "Game started", event_type="start")
        self.game_log.add_event(start_event)

        print(f"DEBUG: Player initialized at location {self.player.current_location}")

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """Load locations and items from a JSON file."""
        with open(filename, 'r') as f:
            data = json.load(f)

        locations = {
            loc['id']: Location(
                location_id=loc['id'],
                brief_description=loc.get('brief_description', "No brief description available."),
                long_description=loc.get('long_description', "No long description available."),
                available_commands=loc.get('available_commands', {}),
                items=loc.get('items', []),
                rooms_contained=loc.get('rooms_contained', []),
                condition_to_unlock=loc.get('condition_to_unlock', None),
                steps_allowed=loc.get('steps_allowed', None),
                npc=loc.get('npc', None),
                puzzle=loc.get('puzzle', None)
            ) for loc in data['locations']
        }

        items = [
            Item(
                name=item['name'],
                start_position=item.get('start_position', -1),
                target_position=item.get('target_position', None),
                target_points=item.get('target_points', 0),
                function=item.get('function', None),
                items_contained=item.get('items_contained', []),
                condition_to_unlock=item.get('condition_to_unlock', None),
                coins=item.get('coins', 0)
            ) for item in data['items']
        ]

        return locations, items

    @staticmethod
    def _load_npcs(filename: str) -> list[NPC]:
        """Load NPCs from a JSON file."""
        with open(filename, 'r') as f:
            data = json.load(f)

        npcs = []
        for npc_data in data.get('npcs', []):
            # Ensure selling_items is always a dictionary
            selling_items = npc_data.get("selling_items", {})

            npcs.append(NPC(
                name=npc_data.get("name", ""),
                dialogue=npc_data.get("dialogue", "No dialogue available."),
                reward_points=npc_data.get("reward_points", 0),
                location=npc_data.get("location"),
                mission_items=npc_data.get("mission_items", []),
                mission_complete_description=npc_data.get("mission_complete_description", ""),
                selling_items=selling_items  # ✅ Now correctly loaded
            ))

        return npcs

    def get_items(self) -> list[Item]:
        """Return list of items associated with the game.
        """
        return self._items

    def get_location(self, loc_id: Optional[int] = None) -> Location | None:
        """Return Location object associated with the provided location ID."""
        if loc_id is None:
            loc_id = self.player.current_location

        loc_obj = self._locations.get(loc_id, None)

        if loc_obj:
            # Ensure items are updated correctly
            loc_obj.items = [item.name for item in self._items if item.start_position == loc_id]

            print(f"DEBUG: Location {loc_id} -> Visited? {loc_obj.visited}")  # ✅ Debugging visit status
            return loc_obj
        else:
            print(f"ERROR: Location ID {loc_id} does not exist.")
            return None

    def handle_special_command(self, user_input: str) -> None:
        """Handle special command that is not in the menu."""

        if user_input.startswith("go "):
            self._handle_movement(user_input)

        elif user_input.startswith("pick up "):
            self._handle_item_pickup(user_input)

        elif user_input.startswith("drop "):
            self._handle_item_drop(user_input)

        elif user_input == "talk":
            self._handle_npc_interaction()

        elif user_input == "solve puzzle":
            self._handle_puzzle_solving()

        elif user_input.startswith("buy "):
            self._handle_item_purchase(user_input)

    def _handle_movement(self, user_input: str) -> None:
        """Handle player movement between locations."""
        loc_obj = self.get_location()

        print(f"DEBUG: Current Location: {self.player.current_location}")
        print(f"DEBUG: Available Commands: {loc_obj.available_commands}")

        normalized_command = user_input.lower().strip()

        # Find a matching command (case-insensitive)
        matched_command = next((cmd for cmd in loc_obj.available_commands if cmd.lower() == normalized_command), None)

        if matched_command:
            new_location_id = loc_obj.available_commands[matched_command]

            print(f"DEBUG: Moving to location {new_location_id}")

            if isinstance(new_location_id, str) and new_location_id.isdigit():
                new_location_id = int(new_location_id)

            self._move_player(new_location_id)  # ✅ Removed 'game_event_log' argument
        else:
            print("You cannot go there.")

    def _move_player(self, new_location_id: int) -> None:
        """Move the player to a new location."""
        if isinstance(new_location_id, int) and new_location_id in self._locations:
            new_location = self._locations[new_location_id]  # Get existing location object

            print(f"DEBUG: Moving player from {self.player.current_location} to {new_location_id}")
            print(f"DEBUG: Before moving - Location {new_location_id} visited? {new_location.visited}")

            # Move player
            self.player.current_location = new_location_id

            # Show the correct description
            if not new_location.visited:
                print(f"DEBUG: Showing long description for {new_location_id}")
                print(new_location.long_description)
                new_location.visited = True  # ✅ Set visited to True
            else:
                print(f"DEBUG: Showing brief description for {new_location_id}")
                print(new_location.brief_description)

            print(
                f"DEBUG: After moving - Location {new_location_id} visited? {new_location.visited}")  # ✅ Check if it updates

        else:
            print(f"ERROR: Location ID {new_location_id} does not exist.")

    def _handle_item_pickup(self, user_input: str) -> None:
        """Handle picking up an item from the environment."""
        item_name = user_input[8:].strip()
        loc_obj = self.get_location()
        if item_name in loc_obj.items:
            item = next((i for i in self._items if i.name == item_name), None)
            if item:
                self.player.add_item(item)
                loc_obj.items.remove(item_name)
                print(f"You picked up {item_name}.")

    def _handle_item_drop(self, user_input: str) -> None:
        """Handle dropping an item from the player's inventory."""
        item_name = user_input[5:].strip()
        item = self.player.remove_item(item_name)
        if item:
            self.get_location().items.append(item_name)
            print(f"You dropped {item_name}.")
        else:
            print(f"You are not carrying {item_name}.")

    def _handle_npc_interaction(self) -> None:
        """Handle interactions with an NPC at the player's current location."""
        npc = next((n for n in self.npcs if n.location == self.player.current_location), None)

        if npc:
            print(f"{npc.name}: {npc.dialogue}")

            # Check if NPC has a mission
            if npc.mission_items and all(self.player.has_item(i) for i in npc.mission_items):
                for item in npc.mission_items:
                    self.player.remove_item(item)
                self.player.score += npc.reward_points
                print(f"You completed {npc.name}'s task and earned {npc.reward_points} points!")

            elif npc.mission_items:
                print(f"{npc.name} needs: {', '.join(npc.mission_items)}. You don't have all the required items yet.")

            # NPC shop interaction
            elif npc.selling_items:
                print(f"{npc.name} has the following items for sale:")
                for item, price in npc.selling_items.items():
                    print(f" - {item}: {price} coins")
        else:
            print("There is no one to talk to here.")

    def _handle_puzzle_solving(self) -> None:
        """Handle solving a puzzle at the player's current location."""
        current_location = self.get_location()

        if current_location.puzzle:
            print(f"You found a puzzle: {current_location.puzzle}")

            # Check if the puzzle requires an item
            required_item = current_location.condition_to_unlock
            if required_item and not self.player.has_item(required_item):
                print(f"You need {required_item} to solve this puzzle.")
                return

            print(f"You solved the puzzle: {current_location.puzzle}!")
            self.player.score += 20  # Example: Reward points for solving a puzzle

            # Remove the required item if it was needed
            if required_item:
                self.player.remove_item(required_item)
        else:
            print("There is no puzzle to solve here.")

    def _handle_item_purchase(self, user_input: str) -> None:
        """Handle buying an item from an NPC shop."""
        found_npc = next((n for n in self.npcs if n.location == self.player.current_location), None)

        if not found_npc or not found_npc.selling_items:
            print("There is no NPC selling items here.")
            return

        item_name = user_input[4:].strip()  # Extract item name from command
        item_price = found_npc.selling_items.get(item_name)

        if not self._can_purchase_item(item_name, item_price):
            return

        self._process_item_purchase(item_name, item_price)

    def _can_purchase_item(self, item_name: str, item_price: Optional[int]) -> bool:
        """Check if the player can purchase the given item."""
        if item_price is None:
            print(f"'{item_name}' is not available for purchase.")
            return False
        if self.player.coins < item_price:
            print(f"You don't have enough coins to buy '{item_name}'.")
            return False
        return True

    def _process_item_purchase(self, item_name: str, item_price: int) -> None:
        """Process the item purchase and update player inventory."""
        self.player.coins -= item_price
        new_item = next((i for i in self._items if i.name.lower() == item_name.lower()), None)

        if new_item:
            self.player.add_item(new_item)
            print(f"You bought {item_name} for {item_price} coins.")
        else:
            print("Something went wrong. Item not found in game data.")

    def handle_command(self, user_input: str, game_event_log: EventList) -> None:
        """Handle player commands such as look, inventory, score, undo, log, and quit."""

        if user_input == "look":
            self._handle_look()

        elif user_input == "inventory":
            self._handle_inventory()

        elif user_input == "score":
            self._handle_score()

        elif user_input == "undo":
            self._handle_undo(game_event_log)

        elif user_input == "log":
            game_event_log.display_events()

        elif user_input == "quit":
            self._handle_quit()

    def _handle_look(self) -> None:
        """Handle the 'look' command.
        Show the long description only the first time the player visits the location.
        On subsequent visits, show the brief description.
        """
        loc_obj = self.get_location()
        if loc_obj is not None:
            if not loc_obj.visited:
                # Show long description for the first visit
                print(loc_obj.long_description)
                loc_obj.visited = True  # Mark the location as visited
            else:
                # Show brief description for subsequent visits
                print(loc_obj.brief_description)

    def _handle_inventory(self) -> None:
        """Display player's inventory and coins."""
        if self.player.inventory:
            print("You are carrying:", ", ".join(item.name for item in self.player.inventory))
        else:
            print("Your inventory is empty.")
        print(f"You have {self.player.coins} coins.")

    def _handle_score(self) -> None:
        """Display the player's score."""
        print(f"Your current score is: {self.player.score}")

    def _handle_undo(self, game_event_log: EventList) -> None:
        """Undo the last action if possible."""
        if not game_event_log.is_empty():
            last_event = game_event_log.last
            if last_event and isinstance(last_event.prev_location, int):
                self.player.current_location = last_event.prev_location
                print(f"You've undone your last action. Back at location {self.player.current_location}.")
                game_event_log.remove_last_event()
            else:
                print("No valid previous location to revert to.")
        else:
            print("Nothing to undo.")

    def _handle_quit(self) -> None:
        """Quit the game."""
        print("You quit the game.")
        self.ongoing = False

    def check_win_condition(self) -> bool:
        """Check if the player has completed enough tasks to win the game."""
        completed_tasks = sum(
            1 for npc in self.npcs if npc.mission_items and all(self.player.has_item(i) for i in npc.mission_items))

        # Ensure step limit isn't exceeded in key areas
        for loc in self._locations.values():
            if loc.steps_allowed is not None and self.moves_made >= loc.steps_allowed:
                print(f"You exceeded the step limit in {loc.brief_description}.")
                return False

        return completed_tasks >= 2


if __name__ == "__main__":

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 0)  # load data, setting initial location ID to 1
    menu = ["look", "inventory", "score", "undo", "log", "quit"]  # Regular menu options available at each location
    while game.ongoing:
        location = game.get_location()
        choice = input("Enter action: ").lower().strip()
        if choice in menu:
            game.handle_command(choice, game_log)
        else:
            game.handle_special_command(choice)
