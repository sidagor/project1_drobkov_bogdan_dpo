
from labyrinth_game import constants
from labyrinth_game import utils

def move_player(game_state: dict, direction: str) -> None:
    current_room = game_state['current_room']
    room_data = constants.ROOMS[current_room]

    if direction in room_data['exits']:
        game_state['current_room'] = room_data['exits'][direction]
        game_state['steps_taken'] += 1
        utils.describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state: dict, item_name: str) -> None:
    current_room = game_state['current_room']
    room_data = constants.ROOMS[current_room]

    if item_name in room_data['items']:
        game_state['player_inventory'].append(item_name)
        room_data['items'].remove(item_name)
        print(f"Вы подняли {item_name}.")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state: dict, item_name: str) -> None:
    inventory = game_state['player_inventory']

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    if item_name == 'torch':
        print("Стало светлее! Теперь вы лучше видите окружение.")
    elif item_name == 'sword':
        print("Вы чувствуете уверенность с мечом в руках.")
    elif item_name == 'bronze_box':
        print("Вы открыли бронзовую шкатулку.")
        if 'rusty_key' not in inventory:
            inventory.append('rusty_key')
            print("Внутри вы нашли rusty_key!")
        else:
            print("Шкатулка пуста.")
    else:
        print(f"Вы не знаете, как использовать {item_name}.")

def get_input(prompt: str = "> ") -> str:
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def show_inventory(game_state: dict) -> None:
    inventory = game_state['player_inventory']

    if inventory:
        print("Ваш инвентарь:", ", ".join(inventory))
    else:
        print("Ваш инвентарь пуст.")
