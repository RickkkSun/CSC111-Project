"""CSC111 Project 1: Text Adventure Game - Event Logger

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

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
from dataclasses import dataclass
from typing import Optional


# TODO: Copy/paste your ex1_event_logger code below, and modify it if needed to fit your game


@dataclass
class Event:
    """
    A node representing one event in an adventure game.

 Instance Attributes:
    - id_num: Integer ID of this event's location.
    - description: Long description of this event's location.
    - next_command: String command that led to this event, None if this is the first game event.
    - next: Reference to the next event in the game, or None if this is the last event.
    - prev: Reference to the previous event in the game, or None if this is the first event.
    - event_type: The type of event ("move", "pickup", "drop", "puzzle", "mission").
    - affected_item: The item affected in this event, if applicable.
    - puzzle_completed: Name of the completed puzzle, if applicable.
    - mission_completed: Name of the completed mission, if applicable.
    """

    # NOTES:
    # This is proj1_event_logger (separate from the ex1 file). In this file, you may add new attributes/methods,
    # or modify the names or types of provided attributes/methods, as needed for your game.
    # If you want to create a special type of Event for your game that requires a different
    # set of attributes, you can create new classes using inheritance, as well.

    id_num: int
    description: str
    prev_location: Optional[int] = None
    next_command: Optional[str] = None
    next: Optional[Event] = None
    prev: Optional[Event] = None
    event_type: Optional[str] = None
    affected_item: Optional[str] = None
    puzzle_completed: Optional[str] = None
    mission_completed: Optional[str] = None


class EventList:
    """
    A linked list of game events.

    Instance Attributes:
        - first: The first event in the list, or None if the linked list is empty.
        - last: The last event in the list, or None if the linked list is empty.
        - steps_taken: Total number of steps taken by the player.
        - completed_puzzles: List of completed puzzles.
        - completed_missions: List of completed NPC missions.

    Representation Invariants:
        - If the list is not empty, the last event's next attribute has to be None.
    """
    first: Optional[Event]
    last: Optional[Event]
    steps_taken: int
    completed_puzzles: list[str]
    completed_missions: list[str]

    def __init__(self) -> None:
        """Initialize a new empty event list."""
        self.first = None
        self.last = None
        self.steps_taken = 0
        self.completed_puzzles = []
        self.completed_missions = []
        self.prev_location = None

    def display_events(self) -> None:
        """Display all events in chronological order."""
        curr = self.first
        while curr:
            event_info = f"Location: {curr.id_num}, Command: {curr.next_command}, Type: {curr.event_type}"
            if curr.affected_item:
                event_info += f", Item: {curr.affected_item}"
            if curr.puzzle_completed:
                event_info += f", Puzzle Completed: {curr.puzzle_completed}"
            if curr.mission_completed:
                event_info += f", Mission Completed: {curr.mission_completed}"
            print(event_info)
            curr = curr.next

    def is_empty(self) -> bool:
        """Return whether this event list is empty."""

        return self.first is None

    def add_event(self, event: Event, command: str = None) -> None:
        """Add the given new event to the end of this event list.
        The given command is the command which was used to reach this new event, or None if this is the first
        event in the game.
        """
        if self.is_empty():
            self.first = event
            self.last = event
            event.prev_location = event.id_num
        else:
            event.prev = self.last
            self.last.next = event
            self.last.next_command = command
            event.prev_location = self.last.id_num
            self.last = event

        if event.event_type == "move":
            self.steps_taken += 1
            if event.prev is not None:
                event.prev_location = event.prev.id_num

        if event.puzzle_completed:
            self.completed_puzzles.append(event.puzzle_completed)

        if event.mission_completed:
            self.completed_missions.append(event.mission_completed)

    def remove_last_event(self) -> None:
        """Remove the last event from this event list.
        If the list is empty, do nothing."""
        if not self.is_empty():
            if self.first == self.last:
                # If only one event exists, reset the event list
                self.first = None
                self.last = None
            else:
                prev_event = self.last.prev

                if self.last.event_type == "move":
                    self.steps_taken = max(0, self.steps_taken - 1)

                if self.last.puzzle_completed:
                    self.completed_puzzles.remove(self.last.puzzle_completed)

                if self.last.mission_completed:
                    self.completed_missions.remove(self.last.mission_completed)

                if prev_event:
                    self.last = prev_event
                    self.last.next = None
                    self.last.next_command = None

    def get_id_log(self) -> list[int]:
        """Return a list of all location IDs visited for each event in this list, in sequence."""

        ids = []
        current = self.first
        while current is not None:
            ids.append(current.id_num)
            current = current.next
        return ids

    def get_steps_taken(self) -> int:
        """Return the number of steps taken by the player."""
        return self.steps_taken

    def get_completed_puzzles(self) -> list[str]:
        """Return a list of all completed puzzles."""
        return self.completed_puzzles

    def get_completed_missions(self) -> list[str]:
        """Return a list of all completed missions."""
        return self.completed_missions

    def get_previous_location(self) -> Optional[int]:
        """Return the player's previous location before the last recorded event, or None if no previous location exists."""
        if self.last and self.last.prev:
            return self.last.prev.id_num  # The location before the last event
        return None


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
