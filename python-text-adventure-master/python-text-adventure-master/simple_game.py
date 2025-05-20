'A simple example game using the text adventure engine.'

from random import randint, choice
from time import sleep
from engine.activity import Activity
from engine.game import Game
from engine.inventory_item import InventoryItem
from engine.place import Place
from engine.event import Event
from engine.transition import Transition


class Simple(Game):
    def __init__(self):
        super(Simple, self).__init__('Happiness')
        self.introduction = 'Welcome to Coding Party'

        # Home
        home = Place('Home', 'You are at home.')
        relaxation_event = Event(0.75, 'Being at home relaxes you.', 5)
        relaxation_event.add_else_events(Event(1, 'A neighbor\'s leaf blower bothers you.', -20))
        home.add_events(relaxation_event)
        # The following events are chained together
        wag_event = Event(0.7, 'Your dog wags its tail.', 5)
        lamp_event = Event(0.5, 'Your dog\'s tail knocks over a lamp.', -10, max_occurrences=2)
        home.add_events(wag_event)    # The dog might wag its tail
        wag_event.chain(lamp_event)   # which could cause the lamp event
        coding_party_invitation = InventoryItem('Coding party invitation', acquire_probability=0.8)
        home.add_items(coding_party_invitation)

        # Left Wall: Activities: play some little games to get hints
        left_wall = Place('Left Wall', 'A fun place to do math')
        left_wall.add_activities(
            Activity('Solve a math problem', self.solve_math_problem),
            Activity('Roll dice for points', self.roll_dice_for_points)
        )

        # Right Wall
        right_wall = Place('Right Wall', 'You may get some mysterious items here.')
        right_wall.add_events(Event(.1, 'Someone talks loudly.', -10, max_occurrences=1))
        programming_book = InventoryItem('Programming Book', acquire_probability=0.8)
        right_wall.add_items(programming_book)

        # Front Door
        front_door = Place('Front Door', 'Be careful not to fall off the wall.')
        front_door.add_events(Event(.1, 'You fall off the wall.', -20, max_occurrences=1))
        front_door.add_events(Event(.1, 'You find a treasure chest.', 20, max_occurrences=1))

        # Coding Party
        coding_party = Place('Coding Party', 'A group of interesting people has gathered to write code.')
        prize_event = Event(0.7, 'You win a prize for most obfuscated code', 50)
        code_prize = InventoryItem('Most Obfuscated Code Prize')
        prize_event.add_items(code_prize)
        coding_party.add_events(
            Event(0.6, 'Someone teaches you some Python', 20),
            Event(0.1, 'A mean person laughs at your code', -20),
            prize_event
        )
        coding_party.add_activities(
            Activity('Enter a coding competition', self.code_challenge),
            Activity('Joke of the Day', self.joke_of_the_day),
        )

        # Transitions
        home.add_transitions(left_wall, right_wall, front_door)
        left_wall.add_transitions(home)
        right_wall.add_transitions(home, Transition(coding_party, programming_book, coding_party_invitation))
        coding_party.add_transitions(right_wall, home)

        # Starting place
        
        self.location = home

    # Activity custom functions

    def solve_math_problem(self) -> int:
        m1 = randint(2, 5)
        m2 = randint(11, 19)
        product = m1 * m2
        answer = int(input(f'Please solve this problem: {m1} * {m2} = ? '))
        change = 10
        if answer == product:
            print('Right!')
        else:
            print('Oops!')
            change = -2
        return change

    def roll_dice_for_points(self) -> int:
        return randint(1, 6) + randint(1, 6)

    def code_challenge(self) -> int:
        from random import random
        num = random()
        print('You compete against another programmer to see who can write the best code.')
        # wwwwwllllt win, lose, tie probability distribution
        if num < 0.5:    # 5/10 chance
            message, change = 'Your program is best and you win the competition.', 40
        elif num < 0.9:  # 4/10 chance
            message, change = 'Another programmer has better code.', -40
        else:            # 1/10 chance
            message, change = 'There is a tie.', 0
        print(message)
        return change

    def joke_of_the_day(self) -> int:
        jokes = (
            ('Why are leopards bad at hiding?', 'Because they are always spotted.'),
            ('What did the pirate say on his 80th birthday?', 'Aye Matey.')
        )
        joke, answer = choice(jokes)
        print(joke)
        sleep(4)
        print(answer)
        sleep(3)  # Pause for laughter
        return 5


if __name__ == '__main__':
    game = Simple()
    game.play()
