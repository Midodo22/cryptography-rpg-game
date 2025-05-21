from random import randint, choice
from time import sleep
from engine.activity import Activity
from engine.game import Game
from engine.inventory_item import InventoryItem
from engine.place import Place
from engine.event import Event
from engine.transition import Transition
from engine.our_activities import factorization_game
from register.login import register

def test_game():
    a = input("input a")
    if(a == 'a'):
        return "Trophy"
    else:
        return 0

class Simple(Game):
    def __init__(self):
        super(Simple, self).__init__('Happiness')
        self.introduction = ''
        
        """
        First level: Register
        """
        dream = Place('Dream', 'Your head feels fuzzy, perhaps you pulled too many all-nighters.\nWho are you?')
        consciousness = InventoryItem('consciousness', acquire_probability=0)
        dream.add_items(consciousness)
        dream.add_activities(
            Activity("Who are you?", register)
        )

        """
        Second level: Decryption
        """
        dungeon = Place('Dungeon', 'You wake up in a dungeon. It smells like sugar. Find a way to escape.')
        relaxation_event = Event(0.5, 'A piece of the wall breaks off, you eat it, it tastes like candy.', 10)
        relaxation_event.add_else_events(Event(0.5, 'A a drop of liquid drips from the ceiling into your mouth, it tastes sour.', -10))
        dungeon.add_events(relaxation_event)
        
        # The following events are chained together
        pick_event = Event(0.1, 'You get bored and decide to pick a pieces of the wall.', 5)
        taste_event = Event(0.5, 'The piece you picked off tastes bad.', -10, max_occurrences = 2)
        dungeon.add_events(pick_event)
        pick_event.chain(taste_event)

        # Left Wall: Activities: play some little games to get hints
        left_wall = Place('Left Wall', 'Start from here, maybe you can get some clues 0v0')
        # TODO: implement problem
        left_wall.add_activities(
            # Activity('Who am I?', self.solve_math_problem),
            # Activity('Test', test_game)
        )

        # Right Wall
        right_wall = Place('Right Wall', 'You may get some mysterious items here.')
        # right_wall.add_events(Event(.1, 'Someone talks loudly.', -10, max_occurrences=1))
        # TODO: key
        right_wall.add_activities(
            # Activity('Test', test_game)
        )

        # Front Door
        front_door = Place('Front door', "The lock won\'t budge.\nWhen I \"left\", I checked my hair multiple times to make sure it looks al\"right\".\nI think it's probably messed up now though.")
        # front_door.add_events(Event(.1, 'You fall off the wall.', -20, max_occurrences = 1))
        # front_door.add_events(Event(.1, 'You find a treasure chest.', 20, max_occurrences = 1))
        front_door.add_activities(
            Activity('Play a factorization game with Tami', factorization_game)
        )
        
        # Transitions
        dream.add_transitions(Transition(front_door, consciousness))
        dungeon.add_transitions(front_door)
        front_door.add_transitions(left_wall, right_wall)
        left_wall.add_transitions(right_wall, front_door)
        right_wall.add_transitions(left_wall, front_door)
        
        # right_wall.add_transitions(front_door, Transition(coding_party, programming_book, coding_party_invitation))
        # coding_party.add_transitions(right_wall, home)
        

        """
        Third level
        """
        # Coding Party
        # coding_party = Place('Coding Party', 'A group of interesting people has gathered to write code.')
        # prize_event = Event(0.7, 'You win a prize for most obfuscated code', 50)
        # code_prize = InventoryItem('Most Obfuscated Code Prize')
        # prize_event.add_items(code_prize)
        # coding_party.add_events(
        #     Event(0.6, 'Someone teaches you some Python', 20),
        #     Event(0.1, 'A mean person laughs at your code', -20),
        #     prize_event
        # )
        # coding_party.add_activities(
        #     Activity('Enter a coding competition', self.code_challenge),
        #     Activity('Joke of the Day', self.joke_of_the_day),
        # )
        
        """
        Fourth level: 2FA
        """

        

        # Starting place
        
        self.location = dream


if __name__ == '__main__':
    game = Simple()
    game.play()