
from labyrinth_game import constants, player_actions


def describe_current_room(game_state: dict) -> None:
    current_room = game_state['current_room']

    if current_room == ('hall_chest' and 'treasure_key'
                        in game_state['player_inventory']):
        current_room = 'hall_door'
        game_state['current_room'] = 'hall_door'

    room_data = constants.ROOMS[current_room]

    print(f"\n== {current_room.upper()} ==")

    print(room_data['description'])

    if room_data['items']:
        print("Заметные предметы:", ", ".join(room_data['items']))

    exits = list(room_data['exits'].keys())
    print("Выходы:", ", ".join(exits))

    if room_data['puzzle'] is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")

def solve_puzzle(game_state: dict) -> None:
    current_room = game_state['current_room']
    room_data = constants.ROOMS[current_room]

    if room_data['puzzle'] is None:
        print("Загадок здесь нет.")
        return

    question, correct_answer = room_data['puzzle']
    print(question)
    user_answer = player_actions.get_input("Ваш ответ: ").lower()

    special_rooms = ['trap_room', 'queen_chamber', 'archive']

    if (user_answer != correct_answer.lower() 
        and current_room not in special_rooms):
        print("Неверно. Попробуйте снова.")
        return

    if user_answer == correct_answer.lower():
        print("Верно! Головоломка решена.")
        room_data['puzzle'] = None

    match current_room:
        case 'queen_chamber':
            if user_answer == 'вы':
                print("Королева замирает, затем ее лицо искажается гримасой боли. ")
                print("НЕТ! Это неправда!' - она с силой швыряет зеркало об пол. ")
                print("Если бы я была так прекрасна, " 
                      "Хлодвиг не заточил бы меня здесь! ")
                print("Он предпочел этим мерзким сокровищам! ЗОЛОТУ! ПЫЛИ! ")
                print("Слезы текут по ее лицу.")

                game_state['player_inventory'].append('queens_key')
                print("Королева швыряет вам queens_key!")

                game_state['player_inventory'].append('vanity_mirror')
                print("Разбитое vanity_mirror падает к вашим ногам!")

                game_state['player_inventory'].append('silver_locket')
                print("Она срывает silver_locket с шеи и бросает вам!")

                print("Королева,рыдая, падает на колени.") 

                room_data['description'] = ('Комната в беспорядке. Королева сидит '
                                             'в углу, тихо рыдая, '
                                             'ее совершенная красота'
                                             'испорчена слезами.'
               )
            else:
               print("Королева не реагирует")


        case 'archive':
            if user_answer == 'да':
                print("\nМагнус издает звук, похожий на смех: 'Ха-ха-ха... "
                      " Очередной одержимый.")
                print("Я - Магнус Архивариус, король Хлодвиг приказал мне изучить "
                      " сокровище, которое ты ищешь.")
                print("Но я совершил ошибку - подошел слишком близко. Теперь "
                      "я не могу умереть.")
                print("Проклятие сокровищ дарует бессмертие всем, кто находится "
                      " рядом с ними. ")
                print("Энергия этих проклятых предметов держит меня "
                      "здесь уже три века.")
                print("Король Хлодвиг сошел с ума после того как нашел их. "
                      "Элрик... бедный Элрик... ")
                print("Он стал их хранителем, а потом и их жертвой. "
                      " Запер себя в тюрьме.")
                print("Я видел, как сокровища уничтожили десятки людей. "
                      " Всех, кто к ним прикасался.")
                print("Прошу тебя, уничтожь их, спаси других!")
                print("И еще, возьми мой кинжал и убей меня. ")
                print("Я понимаю, что я этого не заслужил, но я устал смотреть "
                      "как умирает каждый, кто здесь оказывается. ") 

                if 'magnus_dagger' not in game_state['player_inventory']:
                    game_state['player_inventory'].append('magnus_dagger')
                    print("\nМагнус протягивает вам старый ритуальный кинжал.")
                    print("Вы получили magnus_dagger!")

                    print("\nМагнус: 'Сделай это... и запомни - единственный " 
                          "верный путь - уничтожить это проклятье")
            else:
                if user_answer == 'нет':
                    print("\nМагнус смотрит на вас с удивлением: 'Не за сокровищем? "
                          "Тогда зачем ты здесь?")
                    print("Уходи, пока не стало слишком поздно. "
                          " Это место приносит только страдания.")
                else:
                    print("Магнус качает головой: 'Я не понимаю тебя...'")

        case 'hall':
            if 'treasure_key' not in game_state['player_inventory']:
                game_state['player_inventory'].append('treasure_key')
                print("Вы получили treasure_key!")

            print("Часть стены пропадает, там оказывается дверь с тремя замками...")

            for room_name, room_data in constants.ROOMS.items():
                if 'exits' in room_data:
                    for direction, target_room in room_data['exits'].items():
                        if target_room == 'hall_chest':
                            room_data['exits'][direction] = 'hall_door'
            game_state['current_room'] = 'hall_door'
            describe_current_room(game_state)

        case 'hall_door':
            inventory = game_state['player_inventory']
            required_keys = ['knowledge_key', 'guardian_key', 'queens_key']

            if all(key in inventory for key in required_keys):
                room_data['exits']['north'] = 'treasure_room'
                print("Все три ключа у вас! Дверь открыта, можно идти на north.")
            else:
                missing_keys = [key for key in required_keys
                              if key not in inventory]
                print(f"Не все ключи собраны! Не хватает: "
                      f"{', '.join(missing_keys)}")
                print("Загадка двери не может быть решена "
                      "пока нет всех ключей.")

        case 'trap_room':
            if user_answer == 'шаг шаг шаг':
                print("Ловушка деактивирована! Теперь вы можете безопасно "
                  " перемещаться.")
                print("Открылась потайная двер. Доступен новый проход south")

                current_room = game_state['current_room']
                constants.ROOMS[current_room]['exits']['south'] = 'archive'
            else:
               print("Плита, на которой вы стояли, резко поднялась вверх, "
                     " вас раздавило. ")
               game_state['game_over'] = True
               return

        case 'library':
            if 'silver_key' not in game_state['player_inventory']:
                game_state['player_inventory'].append('silver_key')
                print("Вы получили silver_key! Возможно, он откроет что-то важное.")

        case 'garden':
            print("Фонтан ожил! Вода начала течь, освежая воздух.")
            if 'silver_key' not in game_state['player_inventory']:
                game_state['player_inventory'].append('silver_key')
                print("В струях фонтана вы заметили silver_key!")

        case 'secret_passage':
            print("Потайная дверь открылась! Появился новый выход 'west'.")
            current_room = game_state['current_room']
            constants.ROOMS[current_room]['exits']['west'] = 'prison'

        case 'prison':
            print("Может стоить снять кандалы с этого несчастного, "
                  " кажется он достаточно страдал.")
            print("Используйте silver_key") 

        case _:
            print("Вы чувствуете, что стали мудрее.")


def attempt_open_treasure(game_state: dict) -> None:
    current_room = game_state['current_room']
    room_data = constants.ROOMS[current_room]

    if current_room != 'treasure_room' or 'treasure_chest' not in room_data['items']:
        print("Здесь нет сундука с сокровищами.")
        return

    inventory = game_state['player_inventory']

    if 'treasure_key' in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room_data['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return

    print("Сундук заперт... Ввести код? (да/нет)")
    choice = player_actions.get_input().lower()

    if choice == 'да':
        code = player_actions.get_input("Введите код: ")
        if room_data['puzzle'] and code == room_data['puzzle'][1]:
            print("Код верный! Сундук открыт!")
            room_data['items'].remove('treasure_chest')
            print("В сундуке сокровище! Вы победили!")
            game_state['game_over'] = True
        else:
            print("Неверный код.")
    else:
        print("Вы отступаете от сундука.")

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")
