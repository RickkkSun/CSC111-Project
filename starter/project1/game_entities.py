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
from typing import Optional


@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        id: a number representing the location id
        name: the name of the location
        brief_description: a brief description of the location
        long_description: a long description of the location shown when it's the first time been in this location
        available_commands: available commands in this location
        items: items that can be found in this location
        visited: show whether if the player have visited this location already or not

    Representation Invariants:
        id > 0
    """

    # This is just a suggested starter class for Location.
    # You may change/add parameters and the data available for each Location object as you see fit.
    #
    # The only thing you must NOT change is the name of this class: Location.
    # All locations in your game MUST be represented as an instance of this class.
    id_num: int
    name: str
    brief_description: str
    long_description: str
    available_commands: dict[str, int]
    items: list[str]
    unlock_condition: Optional[str]
    visited: bool
    steps_allowed: Optional[int]

    def __init__(self, location_id, brief_description, long_description, available_commands, items,
                 unlock_condition, visited, steps_allowed) -> None:
        """Initialize a new location.

        """

        self.id_num = location_id
        self.brief_description = brief_description
        self.long_description = long_description
        self.available_commands = available_commands
        self.items = items
        self.unlock_condition = unlock_condition
        self.visited = False
        self.steps_allowed = steps_allowed


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        name: the name of the item
        start_position: the starting position of the player when entering the location where the item is
        target_position: the posiiton of the item
        target_points: the points awarded when obtaining the item

    Representation Invariants:
        start_position > 0
        target_position > 0
        target_points > 0
    """

    # NOTES:
    # This is just a suggested starter class for Item.
    # You may change these parameters and the data available for each Item object as you see fit.
    # (The current parameters correspond to the example in the handout).
    #
    # The only thing you must NOT change is the name of this class: Item.
    # All item objects in your game MUST be represented as an instance of this class.

    name: str
    description: str
    start_position: int
    target_position: int
    target_points: int
    coins: int
    function: Optional[str]

    def __init__(self, name, description, starter_position, target_position, target_points, coins, function):

        self.name = name
        self.description = description
        self.start_position = starter_position
        self.target_position = target_position
        self.target_points = target_points
        self.coins = 0
        self.function = function

# Note: Other entities you may want to add, depending on your game plan:
# - Puzzle class to represent special locations (could inherit from Location class if it seems suitable)
# - Player class
# etc.


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
