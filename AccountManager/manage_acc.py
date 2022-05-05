#help(string) # on Python 3
#....
#DATA
    #ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    #ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
    #ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    #digits = '0123456789'
    #hexdigits = '0123456789abcdefABCDEF'
    #octdigits = '01234567'
    #printable = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
    #punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    #whitespace = ' \t\n\r\x0b\x0c'

import string
import random


lcl_list = list(string.ascii_lowercase)
ucl_list = list(string.ascii_uppercase)
dig_list = list(string.digits)
punc_list = list(string.punctuation)

class Account_handler():
    def register(self, username_input, password_input):

        def create_username(username_input):
            ###
            # This function accepts one string parameter and checks the username 
            # Return string error if username is not valid
            # Return the username if the username is valid
            ###
            if len(username_input) >= 4:
                return username_input
            else:
                return "Your username should be minimum 4 characters long"


        def create_password(password_input):
            ###
            #This function accpets one string parameter, and chekcs the requirements
            #Return string if password is not valid
            #Return the password if password is valid
            ###

            # password needs
            # print("Your password should contain minimum 1 lowercase 1 uppercase 1 digit and should have minimum 8 characters.")
            # function for formulating errors
            def formulate_error(e):
                return(f"Your password should {e}. Please try a new one!")

            #checking length
            if len(password_input) < 8:
                return formulate_error("include minimum 8 characters")
            #checking content
            else:
                u = 0 # Upper case
                l = 0 # Lower case
                d = 0 # Digit
                for c in password_input:
                    #checking for punc
                    if c in punc_list:
                        return formulate_error("not contain punctuations")
                    #checking for minimum 1 uppercase
                    elif c in ucl_list:
                        u = 1
                    #checking for minimum 1 lowercase
                    elif c in lcl_list:
                        l = 1
                    #checking for minimum 1 digit
                    elif c in dig_list:
                        d = 1
                # calling the formulating errors function
                if u == 0:
                    return formulate_error("contain minimum 1 uppercase characters")
                elif l == 0:
                    return formulate_error("contain minimum 1 lowercase letters")
                elif d == 0:
                    return formulate_error("contain minimum 1 digit")
                else:
                    return password_input
        
        
        return (create_username(username_input), create_password(password_input))


    def log_in(self, username_input, password_input, acc_list):
        ###
        # This function takes 3 parameters, username password and acc_list which is a list
        # the acc_list should be a list of all accounts containing username and pasword of each one
        # Return the username if user and password are correct
        # Return a string error if user not recognized7
        ###
        users_pass = ""
        # finding username and it's password
        for acc in acc_list:
            user, passw = acc
            if username_input == user:
                users_pass = passw
                break
        # if username isnt found so its a wrong username so write a new one
        if users_pass != passw:
            return "No such user!"

        # checking if user is the real user by asking for password 
        if password_input != passw:
            return "Wrong password!"
        # Welcoming user
        return username_input

    def guest(self):
        ###
        # This function generates a random guest username
        ###
        pin = random.randint(100000, 999999)
        return f"Guest{pin}"
