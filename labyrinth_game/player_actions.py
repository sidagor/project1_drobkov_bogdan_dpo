
from labyrinth_game import constants, utils


def move_player(game_state: dict, direction: str) -> None:
    current_room = game_state['current_room']
    room_data = constants.ROOMS[current_room]

    if direction in room_data['exits']:
        game_state['current_room'] = room_data['exits'][direction]

        if (game_state['current_room'] == 'hall'and
            'treasure_key'in game_state['player_inventory']):
            game_state['current_room'] = 'hall_door'
        game_state['steps_taken'] += 1
        utils.describe_current_room(game_state)
        utils.random_event(game_state)

    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state: dict, item_name: str) -> None:
    current_room = game_state['current_room']
    room_data = constants.ROOMS[current_room]

    if item_name == 'treasure_chest':
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    if item_name in room_data['items']:
        game_state['player_inventory'].append(item_name)
        room_data['items'].remove(item_name)
        print(f"Вы подняли {item_name}.")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state: dict, item_name: str) -> None:
    """Использует предмет из инвентаря."""
    inventory = game_state['player_inventory']
    current_room = game_state['current_room']

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    match item_name:
        case 'torch':
            print("Стало светлее! Теперь вы лучше видите окружение.")
        case 'sword':
            print("Вы чувствуете уверенность с мечом в руках.")
        case 'bronze_box':
            print("Вы открыли бронзовую шкатулку.")
            if 'rusty_key' not in inventory:
                inventory.append('rusty_key')
                print("Внутри вы нашли rusty_key!")
            else:
                print("Шкатулка пуста.")
        case 'vanity_mirror':
            print("Вы смотрите в разбитое зеркало.")
            print("В треснувшем отражении вы видите искаженные образы.")
        case 'silver_locket':
            print("В серебряном медальоне вы видите портрет молодого Хлодвига.")
            print("На обратной стороне выгравировано: 'Прости меня, Изабелла'")
            print("Кажется, король сожалел о своем выборе...")
        case 'magnus_dagger':
            if current_room == 'archive':
                print("Вы поднимаете кинжал... Магнус смотрит на вас с "
                      "благодарностью.")
                print("'Спасибо... наконец-то свобода...'")
                print("Вы вонзаете кинжал в грудь Магнуса. Его тело "
                      "рассыпается в пыль.")
                print("Из пыли поднимается светящаяся фигура: 'Ты освободил "
                      "меня. Возьми это...'")
                if 'ancient_knowledge' not in game_state['player_inventory']:
                    game_state['player_inventory'].append('ancient_knowledge')
                    print("Вы получили ancient_knowledge!")
                inventory.remove('magnus_dagger')
                print("Кинжал исчезает вместе с Магнусом.")
            else:
                print("Ритуальный кинжал Магнуса. Он просил вас использовать "
                      "его только в архиве.")
        case 'rusty_key':
            if current_room == 'trap_room':
                print("Вы используете ржавый ключ на двери архива...")
                print("Замок со скрипом поддается! Дверь в архив открыта.")
                print("Теперь вы можете пройти на south.")
            else:
                print("Ржавый ключ. Возможно, откроет какую-то дверь.")
        case 'ancient_knowledge':
            print("Древнее знание Магнуса наполняет вас:")
            print("- Сокровища несут проклятие бессмертия")
            print("- Только добровольный отказ может снять проклятие")
            print("Вы понимаете, что должны сделать осознанный выбор в "
                  "treasure_room.")
        case 'silver_key':
            if current_room == 'prison':
                print("Вы используете серебряный ключ на кандалах скелета...")
                print("Кандалы с грохотом падают на пол.")
                print("Из скелета поднимается прозрачная фигура призрака.")
                print("Призрак: 'Спасибо, путник! Ты освободил меня от "
                      "вечного заточения.'")
                print("Призрак: 'Я был стражем сокровищ, но меня предали...'")
                print("Призрак: 'Возьми это в знак благодарности...'")
                if 'ghost_blessing' not in inventory:
                    inventory.append('ghost_blessing')
                    print("Вы получили благословение призрака!")
                inventory.remove('silver_key')
                print("Серебряный ключ рассыпался в пыль, выполнив свое "
                      "предназначение.")
            else:
                print("Серебряный ключ. Выглядит ценным. Возможно, он "
                      "откроет что-то важное.")
        case 'ancient_book':
            print("В древней книге написано: 'Знание - сила'.")
        case 'prisoner_card':
            print("На карточке написано:")
            print("Имя: Элрик Страж")
            print("Звание: Хранитель Сокровищ")
            print("Причина заключения: 'Предательство'")
            print("Дата: 15.03.1523")
            print("Примечание: 'Знает секрет сокровищницы'")
        case 'old_diary':
            print("В дневнике написано: 'Меня предали свои же... Я знал "
                  "слишком много о настоящем сокровище. Оно не в сундуке, "
                  "а в...'")
        case 'rusty_handcuffs':
            print("Ржавые кандалы. Печальное напоминание о судьбе "
                  "заключенного.")
        case 'ghost_blessing':
            print("Вы чувствуете защиту благословения призрака. Элрик "
                  "оберегает вас.")
        case _:
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
