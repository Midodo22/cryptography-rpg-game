from kms.FEncryption import encryption
from kms.GDecryption import decryption

def init_encryption():
    enc_ash()
    enc_page()
    enc_parchment()
    
    return 'Sticky hands'

def enc_ash():
    encryption(b"You pick up a jar of ash from the fireplace.", 
               "kms/data/ash.bin", 
               "kms/data/ash_dek.bin")
    return
    
def dec_ash():
    decryption("kms/data/ash.bin",
               "kms/data/ash_dek.bin")
    
    return 'Bottle of Ash'

def enc_parchment():
    encryption(b"Within the pile of rice paper you find a piece of parchment paper.", 
               "kms/data/parchment.bin", 
               "kms/data/parchment_dek.bin")
    return

def dec_parchment():
    decryption("kms/data/parchment.bin",
               "kms/data/parchment_dek.bin")
    
    return 'Parchment Paper'

def enc_page():
    encryption(b"You see the square of a yellowed piece of paper tucked into the bookshelf.\nYou ", 
               "kms/data/page.bin", 
               "kms/data/page_dek.bin")
    return

def dec_page():
    decryption("kms/data/page.bin",
               "kms/data/page_dek.bin")
    
    return 'Page of a Sorcery Book'