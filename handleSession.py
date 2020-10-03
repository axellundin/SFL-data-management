import runner, sponsor, session
import os, json, shutil

version = 1.0

startup_message = f" \nWelcome to the Spring För Livet event-handler (Version: {version})!\nHere you will be able to handle an event by storing\nrelevant information about runners and sponsors in a database\nand then handling that database. To receive a list of the available\ncommands or the parameters that you are working with, please type 'help'."


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

    THIS_SESSION = session.Session("")
        
    session_is_running = True
    while session_is_running: 
        user_command = input("\n> ")

        user_command = processUserInput(user_command)
        
        # Make sure user did not type nothing into the consol
        if len(user_command) == 0:
            continue
        
        # Process the command tags

        if user_command[0] == 'help':
            listCommands()
        elif user_command[0] == 'q' or user_command[0] == 'quit':
            print("The session is being shutdown...") 
            return 0
        elif user_command[0] == 'loadsession':
            if len(user_command) > 1:
                THIS_SESSION.loadSession(user_command[1])
            else: 
                print("The command 'loadsession' requires a second argument: [SESSION NAME]\nTry again!")
        elif user_command[0] == 'newsession':
            if len(THIS_SESSION.RUNNERS) > 0 or len(THIS_SESSION.SPONSORS)>0:
                print("The current session has information in it. Do you want to ovverride it? [y/n]")
                if input(">> ").lower() == 'y':
                    THIS_SESSION.RUNNERS = []
                    THIS_SESSION.SPONSORS = []
                    print("Done!")
            else:
                print("The current session is already empty!")

        elif user_command[0] == 'copysession':
            pass
        elif user_command[0] == 'removesession':
            if len(user_command) >= 2:
                sessionsdir = os.getcwd() + "/sessions/"
                there_was_session = False
                for subdir, dirs, files in os.walk(sessionsdir):
                    if len(subdir) > len(sessionsdir): 
                        if subdir[len(sessionsdir):] == user_command[1]:
                            # CODE TO REMOVE THE DIRECTORY
                            there_was_session = True
                            shutil.rmtree(subdir, ignore_errors=True)
                if not there_was_session: 
                    print(f"The session {user_command[1]} does not exist.\nTry 'listsessions'")
        elif user_command[0] == 'listsessions':
            sessionsdir = os.getcwd() + "/sessions/"
            there_was_session = False
            for subdir, dirs, files in os.walk(sessionsdir):
                if len(subdir) > len(sessionsdir):
                    there_was_session = True
                    print(f"\n\t- {subdir[len(sessionsdir):]}")
                    
            if not there_was_session:
                print("There are no sessions...")
        elif user_command[0] == 'addrunner':
            # CONTROL THAT THE INPUT HAS THE CORRECT NUMBER OF PARAMETERS AND THAT THEY ARE THE CORRECT TYPE
            if len(user_command) >= 3:
                if type(user_command[1]) == str and type(user_command[2]) == str: 
                    THIS_SESSION.addRunner(user_command[1], user_command[2]) 
                    saveSession(THIS_SESSION)
                else:
                    print("The parameters need to be stings!")
            else:
                print("The required parameters for this command are [FIRST NAME] [LAST NAME]. Try again!")
        elif user_command[0] == 'addsponsorship':
            if len(user_command) >= 7:
                try:
                    if type((int)(user_command[5])) == int and type((int)(user_command[6])) == int: 
                        THIS_SESSION.addSponsorship(user_command[1], user_command[2], user_command[3], user_command[4], user_command[5], user_command[6])
                    THIS_SESSION.updateRunnerInfo() 
                    saveSession(THIS_SESSION)
                except:
                    print("The last two parameters need to be numbers: [LAP VALUE] [MAX VALUE].")
            else: 
                print("The syntax of this command is\n\t'addsponsorship [RUNNER FIRST NAME] [RUNNER LAST NAME] [SPONSOR FIRST NAME] [SPONSOR LAST NAME] [LAP VALUE] [MAX VALUE]'\n") 
        elif user_command[0] == 'removerunner':
            # MAKE SURE COMMAND IS WRITTEN IN CORRECT SYNTAX
            if len(user_command) >= 3:
                THIS_SESSION.removeRunner(user_command[1], user_command[2])
                saveSession(THIS_SESSION)
            else: 
                print("The syntax for this command is: \n\t'removerunner [FIRST NAME] [LAST NAME]\nTry again!")
        elif user_command[0] == 'removesponsorship':
            if len(user_command) >=5:
                THIS_SESSION.removeSponsorship(user_command[1], user_command[2], user_command[3], user_command[4])
                saveSession(THIS_SESSION)
            else:
                print("The syntax for this command is:\n\t'removesponsorship [RUNNER FIST NAME] [RUNNER LAST NAME] [SPONSOR FIRST NAME] [SPONSOR LAST NAME]\nTry again!")
        elif user_command[0] == 'changerunnername':
            if len(user_command) >=5: 
                THIS_SESSION.changeRunnerName(user_command[1], user_command[2], user_command[3], user_command[4])
                saveSession(THIS_SESSION)
            else:
                print("The syntax for this command is:\n\t'changerunnername [OLD FIRST NAME] [OLD LAST NAME] [NEW FIRST NAME] [NEW LAST NAME]\nTry again!")
        elif user_command[0] == 'changerunnernumberoflaps':
            if len(user_command) >=4:
                try:
                    numLaps = int(user_command[3])
                    THIS_SESSION.changeNumLaps(user_command[1], user_command[2], numLaps)
                    saveSession(THIS_SESSION)
                    continue # Break here
                except:
                    print("The last parameter of this command has to be a number: [NUMBER OF LAPS]") 
            else: 
                print("The syntax for this command is:\n\t'changerunnernumberoflaps [FIRST NAME] [LAST NAME] [NUMBER OF LAPS]\nTry again!") 
        elif user_command[0] == 'changesponsorship':
            if len(user_command) >=7:
                try:
                    if type((int)(user_command[5])) == int and type((int)(user_command[6])) == int: 
                        THIS_SESSION.changeSponsorship(user_command[1], user_command[2], user_command[3], user_command[4], user_command[5], user_command[6])
                        saveSession(THIS_SESSION)
                except: 
                    print("The last two parameters need to be numbers: [LAP VALUE] [MAX VALUE]")
            else: 
                print("The syntax for this command is:\n\t'changesponsorship [RUNNER FIST NAME] [RUNNER LAST NAME] [SP    ONSOR FIRST NAME] [SPONSOR LAST NAME] [LAP VALUE] [MAX VALUE]") 
        elif user_command[0] == 'listrunners':
            THIS_SESSION.listRunners()
        elif user_command[0] == 'listsponsors':
            THIS_SESSION.listSponsors()
        elif user_command[0] == 'getpdf':
            pass
        elif user_command[0] == 'savesession':
            saveSession(THIS_SESSION)
        else: 
            print(f"The command '{user_command[0]}' is not a valid command!\nTo find valid commands, please type 'help'")
         

def saveSession(SESSION):
    if SESSION.session_name == "":
        session_name = input("What should I save the session as?\n>").split(" ")[0]
        SESSION.session_name = session_name
        SESSION.saveSession(session_name)
    else:
        SESSION.saveSession(SESSION.session_name)

def processUserInput(user_input):
    output = user_input.lower()
    output = output.split(' ')
    return output

def listCommands():
    # loadsession
    # copysession
    # newsession
    # savesession
    # updatesession
    # removesession
    # listsessions
    # addrunner
    # addsponsorship
    # removerunner
    # removesponsorship
    # changerunnername
    # changerunnernumberoflaps
    # changesponsorship
    # listrunners
    # listsponsors
    # getpdf

    print("---- AVAILIBLE COMMANDS ----\n")
    print("\tloadsession")
    print("\tcopysession")
    print("\tnewsession")
    print("\tsavesession")
    print("\tupdatesession")
    print("\tremovesession")
    print("\tlistsessions")
    print("\taddrunner")
    print("\taddsponsorship")
    print("\tremoverunner")
    print("\tremovesponsorship")
    print("\tchangerunnername")
    print("\tchangerunnernumberoflaps")
    print("\tchangesponsorship")
    print("\tlistrunners")
    print("\tlistsponsors")
    print("\tgetpdf")
    print("\n---- ---- -------- ---- ---\n")
    print("For more specific information, type:\n")
    print("\t '[COMMANDNAME]' \n")
    print("To quit you can at any time type 'quit' or 'q'.\n")


def main(): 
    handleUserRequests() 

if __name__ == '__main__': 
    main()
