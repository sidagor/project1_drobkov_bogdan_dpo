#!/usr/bin/env python3

from labyrinth_game import constants
from labyrinth_game import player_actions
from labyrinth_game import utils

game_state = {
    'player_inventory': [],
    'current_room': 'entrance',
    'game_over': False,
    'steps_taken': 0
}

def main() -> None:
    print("Добро пожаловать в Лабиринт сокровищ!")

    utils.describe_current_room(game_state)

    while not game_state['game_over']:
        command = player_actions.get_input()

if __name__ == "__main__":
    main()

