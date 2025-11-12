#!/usr/bin/env python3

from labyrinth_game import constants
from labyrinth_game import player_actions
from labyrinth_game import utils

def process_command(game_state: dict, command: str) -> None:
    parts = command.split()
    if not parts:
        return
    action = parts[0]
    argument = parts[1] if len(parts) > 1 else ""

    match action:
        case 'look':
            utils.describe_current_room(game_state)
        case 'go' | 'move':
            if argument:
                player_actions.move_player(game_state, argument)
            else:
                print("Укажите направление: go north/south/east/west")
        case 'take':
            if argument:
                player_actions.take_item(game_state, argument)
            else:
                print("Укажите предмет: take torch")
        case 'use':
            if argument:
                player_actions.use_item(game_state, argument)
            else:
                print("Укажите предмет: use torch")
        case 'inventory' | 'inv':
            player_actions.show_inventory(game_state)
        case 'quit' | 'exit':
            game_state['game_over'] = True
            print("Спасибо за игру!")
        case _:
            print("Неизвестная команда. Доступные: "
                  " look, go, take, use, inventory, quit")

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

