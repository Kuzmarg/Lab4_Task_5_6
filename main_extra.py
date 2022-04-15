"""Task 6"""
import game
# Setting up Locations
k2 = game.Room("K2")
k2.set_description("Місце для настільного футболу і більярду. Що? Ви планували тут працювати?")

trapezna = game.Room("Трапезна")
trapezna.set_description("Мммммм. А пахне як...")

church = game.Room("Церква")
church.set_description("Церква св. Софії. Та, сюди теж треба заходити")

it_space = game.Room('ІТ-простір')
it_space.set_description('Ти тут живеш? Ні? Як ти сюди втрапив?')

the_best_bus_stop = game.Room('Автобусна зупинка')
the_best_bus_stop.set_description('Бермудський трикутник 53ого автобуса.')
# Linking the rooms
trapezna.link_room(it_space, 'захід')
it_space.link_room(trapezna, 'схід')

trapezna.link_room(church, 'північ')
church.link_room(trapezna, 'південь')

it_space.link_room(the_best_bus_stop, 'північ')
the_best_bus_stop.link_room(it_space, 'південь')

the_best_bus_stop.link_room(k2,'захід')
k2.link_room(the_best_bus_stop, 'схід')
# Setting up Items and assigning them to rooms
ball = game.Item("Квадратний м'ячик")
ball.set_description('Що це взагалі таке?')
trapezna.set_item(ball)

calendar = game.Item('Календар')
calendar.set_description('Свіжий календар. Хто взагалі їх ще використовує?')
k2.set_item(calendar)

locall = game.Item('Локаль')
locall.set_description('Картка Локаль.')
the_best_bus_stop.set_item(locall)

book = game.Item('Книга')
book.set_description('Що в ІТ спейсі робить послання Павла до ефесян?')
it_space.set_item(book)

aid = game.FirstAidKit()
church.set_item(aid)
# Setting up Characters and assigning them to rooms
zhora = game.Enemy('Жора Хмурий', 'Найкращий гравець в настільний футбол', True)
zhora.set_conversation("Що означає 'я не буду грати'?")
zhora.set_weakness("Квадратний м'ячик")
k2.set_character(zhora)

dart_olezha = game.Enemy('Олежа', 'Самотньо кліпає лабу. Завж\
ди тут, коли б ти не зайшов')
dart_olezha.set_conversation('Я твій батько... Переходь на КН')
dart_olezha.set_weakness('Календар')
it_space.set_character(dart_olezha)

Galya = game.Enemy('Пані Галя', '+10 до зайвої ваги після зустрічі.', True)
Galya.set_conversation("Яке м'ясо. П'ятниця.")
Galya.set_weakness('Локаль')
trapezna.set_character(Galya)

vodii_Tolyan = game.Friend('Анатолій', 'Стоїть на зупинці, щоб рушити, коли ти наблизишся.')
vodii_Tolyan.set_conversation('*крик з автобуса, що віддаляється*: Пані\
 в трапезній контриться локалем. Просто знай це-ееееее.')
the_best_bus_stop.set_character(vodii_Tolyan)

priest = game.Friend('Священик', 'Служба скінчилась 3 години тому, але він все ще тут')
priest.set_conversation('Вітаю. Добре, що ти зайшов. Ти не бачив мою книгу?')
priest.set_favourite('Книга', 'Дякую тобі. Якщо знайдеш, покажи хлопцю в іт-прост\
орі календар. Може, він просто не знає, що вже 2022 рік...')
church.set_character(priest)
# Setting up main starting conditions
current_room = it_space
backpack = []
print('Дійди до К2, просто дійди до К2. Всі персонажі та особ\
и - рандомні, співпадіння - похибка автора.')

# Main loop
while game.FirstAidKit.health != 0:
    # checks endgame conditions
    if game.FirstAidKit.health == 0:
        print('На жаль, ти програв.')
        break
    if current_room == k2 and current_room.get_character() is None:
        print('Ти в К2 і ти переміг. Вітаю! Так, календар тут, ал\
е Олега не врятувати. Колись він доробить лабку...')
        break

    print("\n")
    current_room.get_details()

    inhabitant = current_room.get_character()
    if inhabitant is not None:
        inhabitant.describe()

    item = current_room.get_item()
    if item is not None:
        item.describe()

    # Checks whether the character wants to attack you imminently
    if inhabitant is not None and isinstance(inhabitant, game.Enemy) and inhabitant.imminent_attack:
        command = 'битва'
        inhabitant.talk()
        print('На тебе напали')
    else:
        print('Усі команди - північ, південь, захід, схід, розмова, річ, битва, дарунок.')
        command = input("> ")

    if command in ["північ", "південь", "схід", "захід"]:
        # Move in the given direction
        if command in current_room.directions:
            current_room = current_room.move(command)
        else:
            print('Там нічого немає.')

    elif command == "розмова":
        # Talk to the inhabitant - check whether there is one!
        if inhabitant is not None:
            inhabitant.talk()

    elif command == "битва":
        if inhabitant is not None and isinstance(inhabitant, game.Enemy):
            # Fight with the inhabitant, if there is one
            print("Чим битися будеш?")
            fight_with = input()
            if fight_with in backpack:
                if inhabitant.fight(fight_with) is True:
                    # What happens if you win?
                    print("Ти переміг. Вітання!")
                    current_room.character = None
                else:
                    # What happens if you lose?
                    print("Ти пограв.")
                    game.FirstAidKit.health -= 1
            else:
                print("У тебе нема цього: " + fight_with)
                print("Ти пограв.")
                game.FirstAidKit.health -= 1

        elif isinstance(inhabitant, game.Friend):
            print('Гей, спокійно, це ж друг.')
            # Do I have this item?
        else:
            print("Ні з ким тут битись.")

    elif command == 'дарунок':
        # give a present to the friend character
        if (inhabitant is not None and isinstance(inhabitant, game.Friend)
        and inhabitant.favourite is not None):
            print("Що за дарунок?")
            your_present = input()
            if your_present in backpack:
                if inhabitant.present(your_present) is True:
                    # What happens if you win?
                    print(inhabitant.award)
                    current_room.character = None
                else:
                    # What happens if you lose?
                    print("Нащо мені це?")
            else:
                print("У тебе нема цього: " + your_present)

        # if friend does not have a favourite item
        elif (inhabitant is not None and isinstance(inhabitant, game.Friend)
        and inhabitant.favourite is None):
            print('Та мені нічого не потрібно.')

        # if the character is your enemy
        elif isinstance(inhabitant, game.Enemy):
            print('Ворогам дарунків не роблять.')

        # nothing to present
        else:
            print("Нікому дарувати.")

    elif command == "річ":
        if item is not None:

            # if first aid kit was used
            if not isinstance(item, game.FirstAidKit):
                print("Ти кладеш " + item.get_name() + " у рюкзак")
                backpack.append(item.get_name())
                current_room.set_item(None)

            # other items taken
            else:
                print('Ти підлікувався. Маєш класні шанси)')
                game.FirstAidKit.health += 1
                current_room.set_item(None)
        # nothing to take
        else:
            print("нічого взяти!")
    # wrong command
    else:
        print("Я не знаю цієї команди ")
