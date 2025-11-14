#!/usr/bin/env python3

from labyrinth_game import player_actions, utils


def process_command(game_state: dict, command: str) -> None:
    """Обрабатывает команды, введенные пользователем."""

    parts = command.split()
    if not parts:
        return
    action = parts[0]
    argument = parts[1] if len(parts) > 1 else ""

    direction_commands = ['north', 'south', 'east', 'west']
    if action in direction_commands:
        player_actions.move_player(game_state, action)
        return

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
        case 'solve':
             if game_state['current_room'] == 'treasure_room':
                utils.attempt_open_treasure(game_state)
             else:
                utils.solve_puzzle(game_state) 
        case 'inventory' | 'inv':
            player_actions.show_inventory(game_state)
        case 'help':
            utils.show_help()
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
    """Основная функция игры, управляющая игровым циклом."""
    print("Добро пожаловать в Лабиринт сокровищ!")

    utils.describe_current_room(game_state)

    while not game_state['game_over']:
         process_command(game_state, player_actions.get_input())

if __name__ == "__main__":
    main()

