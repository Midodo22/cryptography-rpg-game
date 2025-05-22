import time

class user:
    def __init__(self, un, pswd):
        self.name = un
        self.password = pswd 
        # maybe encrypt password?
        self.register_time = time.time()
        
    def two_factor_auth(self):
        a = 0
    

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
        
    password = input("\nPlease input your password. \nThe password cannot exceed 20 characters.\nThe password can contain alphabetical, numerical characters, and !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ .\n-------------------------------\n Your password: ")
    while (not check_pswd(password)):
        password = input("\nInvalid input, please input a new password.\nThe password cannot exceed 20 characters.\nThe password can contain alphabetiacal, numerical characters, and !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ .\n-------------------------------\nYour password: ")
    
    new_user = user(name, password)
    
    return "consciousness"


if __name__ == "__main__":
    register()
    # game = Simple()
    # game.play()