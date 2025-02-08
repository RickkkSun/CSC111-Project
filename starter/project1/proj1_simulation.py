"""CSC111 Project 1: Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

This Python module contains code for Project 1 that allows a user to simulate an entire
playthrough of the game. Please consult the project handout for instructions and details.

You can copy/paste your code from the ex1_simulation file into this one, and modify it as needed
to work with your game.

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
from proj1_event_logger import Event, EventList
from adventure import AdventureGame
from game_entities import Location


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    _game: AdventureGame
    _events: EventList

    # TODO: Copy/paste your code from ex1_simulation below, and make adjustments as needed
    def  __init__(self, game_data_file: str, initial_location_id: int, commands: list[str]) -> None:
        """Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """
        self._events = EventList()
        self._game = AdventureGame(game_data_file, initial_location_id, self._events)

        # Add first event (initial location, no previous command)
        initial_location = self._game.get_location()
        first_event = Event(id_num=initial_location.id_num, description=initial_location.long_description)
        self._events.add_event(first_event)

        # Generate the remaining events based on the commands
        self.generate_events(commands, initial_location)

    def generate_events(self, commands: list[str], current_location: Location) -> None:
        """Generate all events in this simulation.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """
        for command in commands:
            print(f"Executing: {command}")
            prev_location_id = self._game.player.current_location  # Store previous location before executing command

            if command in ["look", "inventory", "score", "undo", "log", "quit"]:
                self._game.handle_command(command, self._events)

            else:
                self._game.handle_special_command(command, self._events)

            new_location_id = self._game.player.current_location
            print(f"Moved from {prev_location_id} to {new_location_id}")

            event_type = None
            affected_item = None
            puzzle_completed = None
            mission_completed = None

            # Detect the event type
            if command.startswith("go "):
                event_type = "move"
            elif command.startswith("pick up "):
                item_name = command[8:].strip()
                print(
                    f"DEBUG: Attempting to pick up {item_name} at location {self._game.player.current_location}")
                if self._game.player.has_item(item_name):
                    print(f"You already have {item_name}.")
                    continue
                elif any(item_name.lower() == item.lower() for item in
                             self._game.get_location().items):
                    item_obj = next((item for item in self._game.get_items() if item.name == item_name), None)
                    if item_obj:
                        self._game.player.add_item(item_obj)
                        event_type = "pickup"
                        affected_item = item_name
                    else:
                        print(f"Error: Could not find full item data for '{item_name}'")
                else:
                    print(f"{item_name} is not here.")
                    continue
            elif command.startswith("drop "):
                event_type = "drop"
                affected_item = command[5:]  # Extract item name
            elif command == "talk":
                npc = next((npc for npc in self._game.npcs if npc.location == new_location_id), None)
                if npc:
                    event_type = "mission" if npc.mission_items else "talk"
                    mission_completed = npc.name if npc.mission_items else None
            elif command == "solve puzzle":
                location = self._game.get_location()
                if hasattr(location, "puzzle") and location.puzzle:
                    event_type = "puzzle"
                    puzzle_completed = f"Solved {location.puzzle}"
                    print(f"Puzzle solved: {location.puzzle}")
                else:
                    print("There is no puzzle to solve here.")

            if event_type or (prev_location_id != new_location_id and self._events.get_id_log()[-1] != new_location_id):
                new_event = Event(
                    id_num=new_location_id,
                    description=self._game.get_location().long_description,
                    next_command=command,
                    event_type=event_type,
                    affected_item=affected_item,
                    puzzle_completed=puzzle_completed,
                    mission_completed=mission_completed
                )
                self._events.add_event(new_event, command)

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.

        >>> sim = AdventureGameSimulation('sample_locations.json', 1, ["go east"])
        >>> sim.get_id_log()
        [1, 2]

        >>> sim = AdventureGameSimulation('sample_locations.json', 1, ["go east", "go east", "buy coffee"])
        >>> sim.get_id_log()
        [1, 2, 3, 3]
        """

        # Note: We have completed this method for you. Do NOT modify it for ex1.

        return self._events.get_id_log()

    def run(self) -> None:
        """Run the game simulation and log location descriptions."""
        current_event = self._events.first  # Start from the first event in the list

        while current_event:
            print(current_event.description)
            if current_event is not self._events.last:
                print("You choose:", current_event.next_command)

            current_event = current_event.next


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

    win_walkthrough = [
        "go east",
        "pick up coffee",
        "go west",
        "talk",
        "go north",
        "pick up notebook",
        "pick up Your STUDENT CARD",
        "go south",
        "go south",
        "talk",
        "buy dry noodles",
        "go north"
    ]

    expected_log = [1, 1, 3, 3, 1, 1, 1, 2, 2, 1, 1, 4, 4, 4, 1, 1]
    win_simulation = AdventureGameSimulation('game_data.json', 0, win_walkthrough)
    print(win_simulation.get_id_log())
    assert win_simulation.get_id_log() == expected_log


    print("\n--- Win Walkthrough ---")
    win_simulation.run()

    # Lose demo: Moving in circles without achieving any goal
    lose_demo = ["go east", "go west", "go south", "go north"]
    expected_log = [1, 1, 3, 3, 1, 1, 1, 2, 2]
    lose_simulation = AdventureGameSimulation('game_data.json', 0, lose_demo)
    assert lose_simulation.get_id_log() == expected_log
    print("\n--- Lose Walkthrough ---")
    lose_simulation.run()

    # Inventory demonstration: Picking up and checking items
    inventory_demo = [
        "go north",
        "pick up notebook",
        "inventory",
        "go south"
    ]
    inventory_simulation = AdventureGameSimulation('game_data.json', 1, inventory_demo)
    print("\n--- Inventory Demo ---")
    inventory_simulation.run()

    # Score demonstration: Gaining points from completing missions
    score_demo = ["go east", "pick up notebook", "go west", "talk"]
    score_simulation = AdventureGameSimulation('game_data.json', 1, score_demo)
    print("\n--- Score Demo ---")
    score_simulation.run()

    # Puzzle demonstration: Completing a puzzle
    puzzle_demo = ["go east", "solve puzzle", "go west"]
    puzzle_simulation = AdventureGameSimulation('game_data.json', 1, puzzle_demo)
    print("\n--- Puzzle Demo ---")
    puzzle_simulation.run()
