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

from game_entities import Location, Item
from proj1_event_logger import Event, EventList


# Note: You may add in other import statements here as needed

# Note: You may add helper functions, classes, etc. below as needed


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        _locations: consists descriptions and commands of all accessible floors in the adventure
        _items: consists descriptions and location of every items that may appear during the adventure as weel as the points and coins awarded accordingly



    Representation Invariants:
        - # TODO add any appropriate representation invariants as needed
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: list[Item]
    current_location_id: int  # Suggested attribute, can be removed
    ongoing: bool  # Suggested attribute, can be removed

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
        self._locations, self._items = self._load_game_data(game_data_file)

        # Suggested attributes (you can remove and track these differently if you wish to do so):
        self.current_location_id = initial_location_id  # game begins at this location
        self.ongoing = True  # whether the game is ongoing
        self._inventory = []
        self.steps_remaining = {}

        for loc_id, loc in self._locations.items():
            if loc.steps_allowed:
                self.steps_remaining[loc_id] = loc.steps_allowed
            else:
                self.steps_remaining[loc_id] = None


    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc in data['location']:
            locations[loc['id']] = Location(
                loc['id'],
                loc['name'],
                loc['brief_description'],
                loc.get('long_description', ''),
                loc.get('available_commands', {}),
                loc.get("items", []),
                loc.get('CONDITION NEEDED TO UNLOCK THIS STAGE'),
                loc.get('steps_allowed')
            )

        items = []
        for item_data in data['items']:
            item = Item(item_data['name'],
                        item_data['description'],
                        item_data['start_position'],
                        item_data['target_position'],
                        item_data['target_points'],
                        item_data.get('coins', 0),
                        item_data.get('Function')
                        )
            items.append(item)
        return locations, items

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """
        if loc_id is None:
            return self._locations[self.current_location_id]
        else:
            return self._locations[loc_id]

    def pick_up_item(self, item_name: str):
        """ Pick up an item from the current location
        """
        loc = self.get_location()
        if item_name in loc.items:
            self._inventory.append(item_name)
            loc.items.remove(item_name)
            print(f"You picked up {item_name}.")
        else:
            print(f"{item_name} is not here.")

    def modify_steps(self, step_change: int):
        """ Modify the steps allowed in the current location.
        """
        loc_id = self.current_location_id
        if self.steps_remaining[loc_id] is not None:
            self.steps_remaining[loc_id] += step_change
            print(f"New step limit for {self._locations[loc_id].name}: {self.steps_remaining[loc_id]} steps.")

    def use_item(self, item_name: str):
        """ Use an item from inventory
        """
        if item_name not in self._inventory:
            print(f"YOu don't have {item_name}.")
            return False

        if item_name == "Your TCard":
            print("You unlocked Robarts Library!")
        elif item_name == "XCard":
            print("You unlocked Robarts Library 25F")
        elif item_name == "dry noodles":
            self.modify_steps(10)
            print("You gained 10 extra steps in this room")
        elif item_name == "surstromming":
            self.modify_steps(-self.steps_remaining[self.current_location_id] // 2)
            print("The smell is horrible! You lost half of your remaining steps")

        self._inventory.remove(item_name)
        return True

    def show_inventory(self):
        """ Display collected item
        """
        if self._inventory:
            print("Inventory:", ", ".join(self._inventory))
        else:
            print("Your inventory is empty")

    def can_enter_location(self, location_id: int):
        """ Check if a location is locked and if the player has the required item
        """
        loc = self._locations.get(location_id)
        if loc and loc.unlock_condition:
            if loc.unlock_condition in self._inventory:
                return True
            print(f"You need {location.unlock_condition} to enter {location.name}.")
            return False
        return True

    def check_win_condition(self):
        """ Check if the player has won the game
        """
        if self.current_location_id == 501:
            print("Congratulations! You have won the game!")
            self.ongoing = False


if __name__ == "__main__":

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 1)  # load data, setting initial location ID to 1
    menu = ["look", "inventory", "score", "undo", "log", "quit"]  # Regular menu options available at each location
    choice = None

    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your marks will be based on how well-organized your code is.

        location = game.get_location()

        # TODO: Add new Event to game log to represent current game location
        #  Note that the <choice> variable should be the command which led to this event
        # YOUR CODE HERE
        if game_log.is_empty():
            event = Event(location.id_num, location.brief_description, "", None, None)
        else:
            event = Event(location.id_num, location.brief_description, choice, None, None)

        game_log.add_event(event)

        # TODO: Depending on whether or not it's been visited before,
        #  print either full description (first time visit) or brief description (every subsequent visit) of location
        # YOUR CODE HERE
        if not location.visited:
            print(location.long_description)
            location.visited = True
        else:
            print(location.brief_description)

        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, score, undo, log, quit")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)
        print("- inventory (check you items)")
        print("- quit (end the game)")

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while choice not in location.available_commands and choice not in menu:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        print("========")
        print("You decided to:", choice)

        if choice in menu:
            # TODO: Handle each menu command as appropriate
            # Note: For the "undo" command, remember to manipulate the game_log event list to keep it up-to-date
            if choice == "log":
                game_log.display_events()
            # ENTER YOUR CODE BELOW to handle other menu commands (remember to use helper functions as appropriate)
            elif choice == "inventory":
                game.show_inventory()
            elif choice == "undo":
                if not game_log.is_empty():
                    game_log.remove_last_event()
                    if not game_log.is_empty():
                        game.current_location_id = game_log.last.id_num
                    else:
                        print("You cannnot undo further")
                else:
                    print("You cannnot undo further")
            elif choice == "quit":
                print("Game Over")
                game.ongoing = False
        else:
            # Handle non-menu actions
            if choice.startswith("pick up "):
                item_name = choice[len("pick up"):]
                game.pick_up_item(item_name)
            elif choice.startswith("use "):
                item_name = choice[len("use "):]
            elif choice.startswith("talk to "):
                item_name = choice[len("talk to "):]
            else:
                result = location.available_commands[choice]
                game.current_location_id = result
