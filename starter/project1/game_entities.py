"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - id_num: The unique id number of the location.
        - brief_description: A short description for the location that has been revisited.
        - long_description: A detailed description for the location when visited for the first time.
        - available_commands: A dictionary mapping valid commands to target location id.
        - items: A list of item names available at this location.
        - visited: A boolean value indicating whether the location has been visited or not.
        - rooms_contained: A list of rooms that belong to this location.
        - condition_to_unlock: A string indicating the required condition to access this location.
        - steps_allowed: The number of steps allowed in this location before restrictions apply.
        - npc: The name of an NPC present at this location, if any.
        - puzzle: A description of a puzzle present at this location, if any.

    Representation Invariants:
        - self.id_num >= 0
        - self.steps_allowed is None or self.steps_allowed > 0
        - self.available_commands is not None
        - all(item != "" for item in self.items)
    """
    id_num: int
    brief_description: str
    long_description: str
    available_commands: dict[str, int]
    items: list[str]
    visited: bool = False
    rooms_contained: Optional[List[str]] = None
    condition_to_unlock: Optional[str] = None
    steps_allowed: Optional[int] = None
    npc: Optional[str] = None
    puzzle: Optional[str] = None

    """Initialize a new location.
    """
    def __init__(self, location_id: int, brief_description: str, long_description: str,
                 available_commands: dict[str, int], items: Optional[list[str]] = None,
                 visited: bool = False, rooms_contained: Optional[list[str]] = None,
                 condition_to_unlock: Optional[str] = None, steps_allowed: Optional[int] = None,
                 npc: Optional[str] = None, puzzle: Optional[str] = None) -> None:
        """Initialize a new location.
        """
        self.id_num = location_id
        self.brief_description = brief_description
        self.long_description = long_description
        self.available_commands = available_commands
        self.items = items if items else []
        self.visited = visited
        self.rooms_contained = rooms_contained
        self.condition_to_unlock = condition_to_unlock
        self.steps_allowed = steps_allowed
        self.npc = npc
        self.puzzle = puzzle

@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: The name of the item.
        - start_position: The id of the location where the item starts.
        - target_position: The id of the location where the item needs to be delivered.
        - target_points: The points that the player will earn when delivering the item.
        - function: A string indicating a special effect of the item (e.g., step boost, unlock area).
        - items_contained: A list of items contained within this item (e.g., treasure chest contents).
        - condition_to_unlock: The requirement to pick up or use this item.
        - coins: The number of coins the player receives when using this item, if applicable.

    Representation Invariants:
        - self.start_position >= 0
        - self.target_position is None or self.target_position >= 0
        - self.target_points >= 0
        - self.coins is None or self.coins >= 0
        - self.items_contained is None or all(isinstance(i, str) for i in self.items_contained)
    """
    name: str
    start_position: int
    target_points: int
    target_position: Optional[int] = None
    function: Optional[str] = None
    items_contained: Optional[List[str]] = None
    condition_to_unlock: Optional[str] = None
    coins: Optional[int] = None


@dataclass
class NPC:
    """Represents the Non-Player Character in the game.

    Instance Attributes:
        - name: The name of the NPC.
        - location: The id of the location where the NPC resides.
        - dialogue: The dialogue displayed when the player interacts with the NPC.
        - mission_items: A list of items the NPC requests from the player.
        - reward_points: The points earned by the player when completing the NPC's task.
        - mission_complete_description: A message displayed when the mission is completed.
        - selling_items: A dictionary of items the NPC sells with their respective prices.

    Representation Invariants:
        - self.location is None or self.location >= 0
        - self.reward_points >= 0
        - self.selling_items is None or all(isinstance(item, str) and isinstance(price, int) and price >= 0
          for item, price in self.selling_items.items())
    """
    name: str
    reward_points: int = 0
    dialogue: Optional[str] = None
    location: Optional[int] = None
    mission_items: Optional[List[str]] = None
    mission_complete_description: Optional[str] = None
    selling_items: Optional[Dict[str, int]] = None


# Note: Other entities you may want to add, depending on your game plan:
# - Puzzle class to represent special locations (could inherit from Location class if it seems suitable)
# - Player class
# etc.

@dataclass
class Player:
    """Represents the player in the game.

    Instance Attributes:
        - current_location: The id of the location where the player is currently located.
        - inventory: A list of items the player is carrying.
        - score: The player's current score.
        - coins: The number of coins the player has collected.

    Representation Invariants:
        - self.current_location >= 0
        - self.score >= 0
        - self.coins >= 0
    """
    current_location: int
    inventory: List[Item]
    score: int
    coins: int = 0

    def __init__(self, start_location: int, inventory: list, coins: int, score: int) -> None:
        self.current_location = start_location
        self.inventory = inventory
        self.coins = coins
        self.score = score

    def add_item(self, item: Item) -> None:
        """Add an item to the player's inventory."""
        self.inventory.append(item)

    def remove_item(self, item_name: str) -> Optional[Item]:
        """Remove an item from the player's inventory by name."""
        for item in self.inventory:
            if item.name == item_name:
                self.inventory.remove(item)
                return item
        return None

    def has_item(self, item_name: str) -> bool:
        """Check if the player has an item with the given name."""
        return any(item.name == item_name for item in self.inventory)

if __name__ == "__main__":
    pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })
