import time
import pyotp
import qrcode
import string
import random

def pad_base32(key):
    while(len(key) % 8 != 0):
        randomLetter = random.choice(string.ascii_letters)
        key += randomLetter
    
    for i in range(8):
        randomLetter = random.choice(string.ascii_letters)
        key += randomLetter
    
    return key

def gen_qr(uri):
    qrcode.make(uri).save("qr.png")

class user:
    def __init__(self, un, pswd):
        self.name = un
        self.password = pswd 
        # maybe encrypt password?
        self.register_time = time.time()
        self.key = pad_base32(self.name)
        
    def two_factor_auth(self):
        # generate google auth
        uri = pyotp.totp.TOTP(self.key).provisioning_uri(
        name = 'mido',
        issuer_name = 'cryptography_project')
        
        gen_qr(uri)
        
        # verify
        totp = pyotp.TOTP(self.key)
        print(totp.now())
        user_input_otp = input("Enter OTP: ")
        if totp.verify(user_input_otp):
            print("OTP verified. Access granted.")
        else:
            print("OTP verification failed. Access denied.")

if __name__ == "__main__":
    mido = user("Mido", "test1234")
    mido.two_factor_auth()