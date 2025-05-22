from random import randint, choice
from time import sleep
from engine.activity import Activity
from engine.game import Game
from engine.inventory_item import InventoryItem
from engine.place import Place
from engine.event import Event
from engine.transition import Transition
from engine.our_activities import factorization_game, dice_game
import register.login as rl
from kms.AExportPublicKey import export_kms_public_key
from kms.BGenerateCsr import generate_kms_signed_csr
from kms.CGetCert import get_cert_from_cas
from kms.DVerifyCert import verify_run
from kms.FEncryption import encryption
from kms.GDecryption import decryption
import kms.encryptDecrypt as encdec

class Simple(Game):
    def __init__(self):
        super(Simple, self).__init__('Sanity')
        self.introduction = ''
        
        """
        First level: Register
        """
        dream = Place('Dream', 'Your head feels fuzzy, perhaps you pulled too many all-nighters.\nWho are you?')
        initial_san = Event(1, 'Initializing sanity...', 100, max_occurrences = 1)
        dream.add_events(initial_san)
        consciousness = InventoryItem('consciousness', acquire_probability = 0, description = 'You gained consciousness in the dungron.')
        dream.add_items(consciousness)
        dream.add_activities(
            Activity("Who are you?", rl.register)
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

        # Left Wall: get public key
        left_wall = Place('Left Wall', 'Start from here, maybe you can get some clues 0v0')
        public_key = InventoryItem('Public Key', 0, 'It can be used to encrypt data.')
        left_wall.add_items(public_key)
        left_wall.add_activities(
            Activity('A block in the wall looks out of place, take a look?', export_kms_public_key)
        )

        # Right Wall: get csr
        right_wall = Place('Right Wall', 'You may get some mysterious items here.')
        csr = InventoryItem('CSR', 0, 'A certificate signing request, sent from applicant to a certificate authority to apply for a digital identity certificate.')
        right_wall.add_items(csr)
        right_wall.add_activities(
            Activity('There\'s a small window on the wall, try calling out for someone?', generate_kms_signed_csr)
        )

        # Front Door
        front_door = Place('Front door', "The door is made of chocolate.\nWhen I \"left\", I checked my hair multiple times to make sure it looks al\"right\".\nI think it's probably messed up now though.")
        # front_door.add_events(Event(.1, 'You fall off the wall.', -20, max_occurrences = 1))
        # front_door.add_events(Event(.1, 'You find a treasure chest.', 20, max_occurrences = 1))
        cert = InventoryItem('Unlocked Lock', 0, 'You were able to unlock the lock on the door with the key you have required.')
        # sticky_hands = InventoryItem('Sticky hands', 0, 'You opened the door leading to the room, but it\'s made of sugar and made your hands sticky.')
        front_door.add_items(cert)
        front_door.add_activities(
            Activity('Play a factorization game with Tami', factorization_game),
            Activity('Unlock door (This might take a while)', get_cert_from_cas)
        )
        
        # Transitions
        dream.add_transitions(Transition(front_door, consciousness))
        dungeon.add_transitions(front_door)
        front_door.add_transitions(left_wall, right_wall)
        left_wall.add_transitions(right_wall, front_door)
        right_wall.add_transitions(left_wall, front_door)

        """
        Third level
        """
        
        candy_house = Place('House of Candy', 'You make it out of the dungeon and arrive in a gingerbread house.\nThe walls of made of gingerbread cookies, the windows of candy, and the furniture of chocolate, fondant, sugar candy, and cake.')
        
        fireplace = Place('Fireplace', 'A small fire sparks in the fireplace made of sugar.')
        fire_event = Event(0.2, "A drop of hot sugar falls off the fireplace and burns you.", -20)
        fireplace.add_events(fire_event)
        ash = InventoryItem('Bottle of Ash', 0, 'Bottle of ash from the fireplace, maybe you can use this to write something?')
        fireplace.add_items(ash)
        fireplace.add_activities(
            Activity('There\'s a small jar on top of the fireplace, use it to pick up some ash?', encdec.dec_ash)
        )
        
        table = Place('Table', 'You take a look at the rice paper on the table made of a huge cookie sandwich.\nThere seems to be clues on how to unlock the door.')
        parchment = InventoryItem('Parchment Paper', 0, 'Seems like you can write on it with the ash.')
        table.add_items(parchment)
        table.add_activities(
            Activity('Rummage through the papers', encdec.dec_parchment),
            Activity('Play a dice game', dice_game)
        )
        
        shelf = Place('Shelf', 'You walk over to the shelf made of crackers.\nMaybe one of the books can help you.')
        magic_page = InventoryItem('Page of a Sorcery Book', 0, 'It has a spell for teleportation, but you\'ll need paper and pen to draw the magic circle.')
        shelf.add_items(magic_page)
        shelf.add_activities(
            Activity('Take a closer look at the shelf', encdec.dec_page)
        )
        
        book1 = Place('Book 1', 'The book is titled \"Cryptography Engineering: Design Principles and Practical Applications\". It looks quite complicated.')
        book1_event = Event(0.3, "You read \"Cryptography Engineering: Design Principles and Practical Applications\" and learned something new.", 20)
        book1_event.add_else_events(Event(0.3, "You read \"Cryptography Engineering: Design Principles and Practical Applications\" and couldn\'t understand finite fields, you feel frustrated.", -10))
        book1.add_events(book1_event)
        
        book2 = Place('Book 2', 'The book is titled \"Algebra for Cryptologists\". You\'ve never been good at math.')
        book2_event = Event(0.3, "You read \"Algebra for Cryptologists\" and learned something new.", 20)
        book2_event.add_else_events(Event(0.3, "You read \"Algebra for Cryptologists\" and couldn\'t solve a problem in the book, you feel frustrated.", -10))
        book2.add_events(book2_event)
        
        book3 = Place('Book 3', 'The book is titled \"Hansel and Gretel\". Sounds weirdly familiar.')
        book3_event = Event(1, "You read \"Hansel and Gretel\" and enjoyed the story.", 50, max_occurrences = 1)
        book3.add_events(book3_event)
        
        door = Place('Door', 'You can leave through this door, but it seems to be locked.')
        
        # Transitions
        front_door.add_transitions(Transition(candy_house, cert))
        candy_house.add_transitions(fireplace, table, shelf)
        fireplace.add_transitions(table, shelf)
        table.add_transitions(fireplace, shelf)
        shelf.add_transitions(table, fireplace, book1, book2, book3)
        book1.add_transitions(shelf, book2, book3)
        book2.add_transitions(shelf, book1, book3)
        book3.add_transitions(shelf, book1, book2)
        door.add_transitions(fireplace, table, shelf)
        
        """
        Fourth level: 2FA
        """
        home = Place('Home', 'You draw a magic circle to teleport home using the ash and parchment paper.\nFinally having escaped the weird candy house, you make it home, but you don\'t have your keys on you.\n')
        door = Place('Door', 'You turn the doorknob to the front door. It\'s locked.')
        window = Place('Window', 'You look in the window, your mom is cooking dinner but she doesn\'t notice you.')
        garden = Place('Garden', 'You rummage around the flower pots in the garden but to your dismay, it seems that someone has taken the hidden backup key.')
        doorbell = Place('Doorbell', f'You push the doorbell. Your grandma comes over but doesn\'t seem to recognize you. You have to find some way to prove to her that you\'re {rl.new_user.name}.')
        grandma = Place('Grandma', 'Grandma says you can prove your identity by doing Two-Factor Authentication. You didn\'t know grandma was into cryptography but they do say you\'re never too old to learn.')
        home_pass = InventoryItem('pass', acquire_probability = 0, description = 'Grandma recognizes you, you can go home now.')
        grandma.add_items(home_pass)
        grandma.add_activities(
            Activity('Two factor authentication', rl.new_user.verify_2fa)
        )
        
        end = Place('Enter house', 'Welcome home! You have completed the game!')
        
        # Transitions
        fireplace.add_transitions(Transition(home, ash, parchment, magic_page))
        table.add_transitions(Transition(home, ash, parchment, magic_page))
        shelf.add_transitions(Transition(home, ash, parchment, magic_page))
        door.add_transitions(Transition(home, ash, parchment, magic_page))
        
        home.add_transitions(door, window, garden)
        window.add_transitions(door, home, garden)
        garden.add_transitions(door, window, home)
        door.add_transitions(window, garden, doorbell)
        grandma.add_transitions(door, window, garden, doorbell, Transition(end, home_pass))
        doorbell.add_transitions(door, window, garden, grandma)

        # Starting place
        
        self.location = table
        self.destination = end


if __name__ == '__main__':
    game = Simple()
    game.play()