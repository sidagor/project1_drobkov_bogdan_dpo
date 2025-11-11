from labyrinth_game import constants

def describe_current_room(game_state: dict) -> None:
    current_room = game_state['current_room']
    room_data = constants.ROOMS[current_room]

    print(f"\n== {current_room.upper()} ==")

    print(room_data['description'])

    if room_data['items']:
        print("Заметные предметы:", ", ".join(room_data['items']))

    exits = list(room_data['exits'].keys())
    print("Выходы:", ", ".join(exits))

    if room_data['puzzle'] is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")
