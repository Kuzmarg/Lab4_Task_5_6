"""Task 5-6"""

class Item:
    """Represents an item in the room"""
    def __init__(self, itemname: str) -> None:
        self.item_name = itemname
        self.description = None

    def set_description(self, description: str) -> None:
        """Set a description to the item"""
        self.description = description

    def get_name(self):
        """Returns the item's name"""
        return self.item_name

    def describe(self):
        """Describes the item"""
        print(f'{self.item_name.capitalize()} - {self.description}')

class Character:
    """Represents a character"""
    def __init__(self, name: str, description: str) -> None:
        self.character_name = name
        self.description = description
        self.conversation = None

    def set_conversation(self, conversation: str) -> None:
        """Sets the conversation with the character"""
        self.conversation = conversation

    def talk(self) -> None:
        """Prints the talk phrase"""
        print(f'Персонаж каже: "{self.conversation}"')

    def describe(self) -> None:
        """Prints a description of a character"""
        print(f'{self.character_name} - {self.description}')

class Enemy(Character):
    """Represents a character in the game"""
    defeated_enemies = 0
    Zhora_defeated = False

    def __init__(self, name: str, description: str, imminent_attack: bool = False) -> None:
        super().__init__(name, description)
        self.weakness = None
        self.imminent_attack = imminent_attack

    def fight(self, item: str) -> bool:
        """Returns True if you win, False - otherwise"""
        if self.weakness == item:
            Enemy.defeated_enemies += 1
            return True
        return False

    def set_weakness(self, item: str) -> None:
        """Sets a weakness"""
        self.weakness = item

    @staticmethod
    def get_defeated():
        """Shows how many enemies were killed"""
        return Enemy.defeated_enemies

class Room:
    """Represents a room"""
    def __init__(self, name) -> None:
        self.name = name
        self.directions = {}
        self.description = None
        self.character = None
        self.item = None

    def set_description(self, description: str) -> None:
        """Sets a description to the room"""
        self.description = description

    def link_room(self, room, direction: str) -> None:
        """Links a room to the given direction"""
        self.directions[direction] = room

    def set_character(self, character: Enemy) -> None:
        """Sets a character to the room"""
        self.character = character

    def set_item(self, item: Item) -> None:
        """Sets an item to the room"""
        self.item = item

    def get_details(self):
        """Prints the description of a room"""
        print(self.description)
        if self.item is not None:
            print(f'Річ: {self.item.item_name}')
        if self.character is not None:
            print(f'Персонаж: {self.character.character_name}')
        if self.directions != {}:
            print('Напрямки:')
            print('\n'.join([f'{j} - {k.name}' for j,k in self.directions.items()]))

    def get_character(self):
        """Returns the room's character"""
        return self.character

    def get_item(self):
        """Returns the room's item"""
        return self.item

    def move(self, direction: str):
        """Returns a new room"""
        return self.directions[direction]

# All the following classes are for task 6

class Friend(Character):
    """Represents a friend"""
    def __init__(self, name: str, description: str) -> None:
        super().__init__(name, description)
        self.favourite = None
        self.award = None

    def present(self, item: str) -> bool:
        """Returns True if you gave a True present, False - otherwise"""
        if self.favourite == item:
            return True
        return False

    def set_favourite(self, favourite: str, award: str) -> None:
        """Sets a favourite thing"""
        self.favourite = favourite
        self.award = award

class FirstAidKit(Item):
    """First aid kit"""
    health = 1

    def __init__(self) -> None:
        super().__init__('Аптечка')
        self.description = f"Збільшує здоров'я на 1.\
 Здоров'я зараз - {FirstAidKit.health}"
