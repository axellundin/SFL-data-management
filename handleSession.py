import runner, sponsor, session
import os, json

version = 1.0

startup_message = f" Welcome to the Spring För Livet event-handler (Version: {version})!\nHere you will be able to handle an event by storing\nrelevant information about runners and sponsors in a database\nand then handling that database. To receive a list of the available\ncommands or the parameters that you are working with, please type 'help'. "


def testCode():
    # Open new session from existing files: 
    SFL_SESSION = session.Session("testsession", MODE='READ') 
    # Save the session as a new session  
    SFL_SESSION.saveSession()

def handleUserRequests():
    # Welcome the user to the user interface and give them the options
    # to receive help and start them off with the process of handling the event
    
    print(startup_message)

    # Loop

    session_is_running = True
    while session_is_running: 
        user_command = input("\n> ")

        processUserInput(user_command)
        
        # Make sure user did not type nothing into the consol
        if len(user_command) == 0:
            continue
        
        # Process the command tags

        if user_command[0] == 'help':
            pass
        elif user_command[0] == 'q':
            pass
        elif user_command[0] == 'loadsesion'
            pass 
        elif user_command[0] == ''
            pass
        else: 
            print(f"The command {user_command[0]} is not a valid command!\nTo find valid commands, please type 'help'")
         

def processUserInput(user_input):
    user_input = user_input.lower
    user_input = user_input.split()

def listCommands():
    # help-command

    # readSession

    # addRunner

    # addSponsorship

    # 

def main(): 
    testCode() # For now only static tests  



if __name__ == '__main__': 
    main()
