import time
from engine.inventory_item import InventoryItem
import pyotp
import qrcode
import string
import random

def gen_qr(uri):
    qrcode.make(uri).save("qr.png")
    
def pad_base32(key):
    while(len(key) % 8 != 0):
        randomLetter = random.choice(string.ascii_letters)
        key += randomLetter
    
    for i in range(8):
        randomLetter = random.choice(string.ascii_letters)
        key += randomLetter
    
    return key

class user:
    def __init__(self, un, pswd):
        self.name = un
        self.password = pswd 
        # maybe encrypt password?
        self.register_time = time.time()
        self.key = pad_base32(self.name)
        
    def init_2fa(self):
        # generate google auth
        uri = pyotp.totp.TOTP(self.key).provisioning_uri(
        name = 'cryptography_project',
        issuer_name = self.name)
        
        gen_qr(uri)
        
    def verify_2fa(self):
        # verify
        totp = pyotp.TOTP(self.key)
        print(totp.now())
        
        user_input_otp = input("Enter OTP: ")
        if totp.verify(user_input_otp):
            print("OTP verified. Access granted.")
            return "pass"
        else:
            print("OTP verification failed. Access denied.")
            return 0
        
    
new_user = user('init', 'init')

def check_name(name):
    if len(name) > 20:
        return False
    
    return name.isalnum()

def check_pswd(pswd):
    if len(pswd) > 20:
        return False
    
    for c in pswd:
        if ord(c) < 32 or ord(c) > 127 or c == ' ':
            return False
        
    return True

def register():
    name = input("Please input your username.\nThe username can only contain alphabetical and numerical characters.\nIt cannot contain spaces, special characers, or exceed 20 characters.\n-------------------------------\nYour preferred username: ")
    while (not check_name(name)):
        name = input("\nInvalid input, please input a new name.\nThe username can only be in English and cannot exceed 20 characters.\n-------------------------------\nYour new username: ")
    new_user.name = name
    
    time.sleep(0.5)
    password = input("\nPlease input your password. \nThe password cannot exceed 20 characters.\nThe password can contain alphabetical, numerical characters, and !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ .\n-------------------------------\n Your password: ")
    while (not check_pswd(password)):
        password = input("\nInvalid input, please input a new password.\nThe password cannot exceed 20 characters.\nThe password can contain alphabetiacal, numerical characters, and !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ .\n-------------------------------\nYour password: ")
    
    new_user.password = password
    new_user.init_2fa()
    
    return "consciousness"



if __name__ == "__main__":
    # register()
    new_user.init_2fa()
    # game = Simple()
    # game.play()