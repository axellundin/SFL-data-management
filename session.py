import sponsor, runner
import json, os

def runnerENCODE(runner):
    runner_info = {
            "firstname": runner.first_name, 
            "lastname": runner.last_name, 
            "lapvalue":runner.value_per_lap, 
            "numberoflaps": runner.number_of_laps
            }   
    sponsor_list = [] 
    for sponsor in runner.sponsor_list:
        sponsor_tags = {
                "firstname": sponsor[0].first_name, 
                "lastname": sponsor[0].last_name, 
                "valueperlap": sponsor[1], 
                "maxval": sponsor[2]
                }
        sponsor_list.append(sponsor_tags)

    OUTPUTFORMAT = []
    OUTPUTFORMAT.append(runner_info)
    OUTPUTFORMAT.append(sponsor_list) 
    
    return OUTPUTFORMAT

def sponsorENCODE(sponsor):
    sponsor_info = {
            "first_name": sponsor.first_name, 
            "last_name": sponsor.last_name, 
            "topay": sponsor.TO_PAY,
            "takenpart": sponsor.HAS_TAKEN_PART
            }
    return sponsor_info

def encodeToJSON(session_name, RUNNERS, SPONSORS):
    rootdir = os.getcwd() 
    sessionsdir = rootdir + "/sessions/"

    # CREATE A CORRECT NAME
    names_that_exist = []
    for subdir, dirs, files in os.walk(sessionsdir):
        if subdir != sessionsdir:
            name = subdir[len(sessionsdir):]
            names_that_exist.append(name)
    
    number_of_copys=0

    while session_name in names_that_exist:
        number_of_copys+=1
        if number_of_copys>1:
            session_name = session_name[:len(session_name) - len(str(number_of_copys-1))] + (str) (number_of_copys)
        else: 
            session_name = session_name +(str) (number_of_copys)
    print(f"Session saved as {session_name} at {sessionsdir + session_name}...")
    
    # CREATE FOLDER
    
    os.mkdir(sessionsdir + session_name) 
    
    # FORMAT INFORMATION ABOUT RUNNERS
        
    json_runner_formatted = []
    for runner in RUNNERS:
        json_runner_formatted.append(runnerENCODE(runner))
    # FORMAT INFORMATION ABOUT SPONSORS

    json_sponsor_formatted = []
    for sponsor in SPONSORS: 
        json_sponsor_formatted.append(sponsorENCODE(sponsor))

    # WRITE TO runners.json
    directory = sessionsdir + session_name
    with open(directory + "/runners.json", 'w') as runnersFile:
        json.dump(json_runner_formatted, runnersFile, indent=2)

    # WRITE TO sponsors.json
    with open(directory + "/sponsors.json", "w") as sponsorsFile:
        json.dump(json_sponsor_formatted, sponsorsFile, indent=2)
    
    # DISPLAY THE RESULT IN THE TERMINAL 


def decodeFromJSON(session_name):
    # INIT RUNNERS LIST
    RUNNERS = []

    # INIT SPONSORS LIST
    SPONSORS = []

    # SEE IF THE SESSION EXISTS:
    rootdir = os.getcwd()
    sessionsdir = rootdir + "/sessions/"

    session_was_found = False
    for subdir, dirs, files in os.walk(sessionsdir):
        if subdir != sessionsdir:
            if subdir[len(sessionsdir):] == session_name:
                session_was_found = True
                with open(sessionsdir +session_name + "/runners.json", "r") as runnersFile:
                    runner_list = json.loads(runnersFile.read())

    if not session_was_found: 
        print(f"The session {session_name} could not be found")
        return None, None
    for new_runner in runner_list: 
        NEW_RUNNER = runner.Runner(new_runner[0].get("firstname"), new_runner[0].get("lastname")) 
        NEW_RUNNER.value_per_lap = new_runner[0].get("lapvalue") 
        NEW_RUNNER.number_of_laps = new_runner[0].get("numberoflaps")
        
        for sponsorship in new_runner[1]: 
            NEW_RUNNER.addSponsorship(sponsorship.get("firstname"), sponsorship.get("lastname"), sponsorship.get("valueperlap"), sponsorship.get("maxval"))
        RUNNERS.append(NEW_RUNNER)

    return RUNNERS, updateSponsorList(RUNNERS) 

def updateSponsorList(RUNNERS):
    SPONSORS = []

    for runner in RUNNERS:
        for new_sponsor in runner.sponsor_list: 
            sponsor_was_registered = False
            for added_sponsor in SPONSORS: # CHECK IF THE SPONSOR HAS ALREADY BEEN REGISTERED
                if added_sponsor.first_name == new_sponsor[0].first_name and added_sponsor.last_name ==  new_sponsor[0].last_name: 
                    sponsor_was_registered = True
                    added_sponsor.TO_PAY += min(new_sponsor[1] * runner.number_of_laps, new_sponsor[2]) # LIMIT THE MAXIMUM SPONSORSHIP IF NECESSARY 
                    break
            if not sponsor_was_registered:
                new_sponsor[0].TO_PAY = min(new_sponsor[1] * runner.number_of_laps, new_sponsor[2]) # LIMIT THE MAXIMUM SPONSORSHIP IF NECESSARY 
                SPONSORS.append(new_sponsor[0])

    return SPONSORS



class Session():
    ''' This is a class that holds information about a complete session of the 
    SPRING FÖR LIVET event. The class variables include the list of runners with their
    respective information, as well as a list of sponsors with relevant connections to 
    the runners. '''

    def __init__(self, session_name, MODE='REGULAR'):
        
        self.session_name = session_name
        self.SPONSORS = []
        self.RUNNERS = []
        if MODE=='REGULAR':
            pass # THIS DOES NOT DO ANTTHING ANYMORE
        elif MODE=='READ':
            while True:
                session_name = input("Please enter the name of the session that you would like to enter:\n")
                self.RUNNERS, self.SPONSORS = decodeFromJSON(session_name)
                if self.RUNNERS == None or self.SPONSORS == None:
                    continue
                else: 
                    break


    def addRunner(self, first_name, last_name):
        NEW_RUNNER = runner.Runner(first_name, last_name)
        self.RUNNERS.append(NEW_RUNNER)
        print(f"The runner {first_name} {last_name} was added to the list of runners!")

    def removeRunner(self, first_name, last_name):
        for runner in self.RUNNERS:
            if runner.first_name == first_name and runner.last_name == last_name:
                print(f"Runner {runner.first_name} {runner.last_name} was removed from the list of runners...")
                self.RUNNERS.remove(runner)
                return None
        print(f"The runner {runner.first_name} {runner.last_name} could not be found!")

    def addSponsorship(self, runner_FN, runner_LN, sponsor_FN, sponsor_LN, value_per_lap, maxcost):
        for runner in self.RUNNERS:
            if runner.first_name == runner_FN and runner.last_name == runner_LN:
                runner.addSponsorship(sponsor_FN, sponsor_LN, value_per_lap, maxcost) 
                self.SPONSORS = updateSponsorList(self.RUNNERS) # UPDATE THE SPONSOR LIST
                print("The sponsorship was added!")
                return None
        print("The sponsorship could not be found!")
    
    def changeRunnerName(self, old_FN, old_LN, new_FN, new_LN):
        runner_was_found = False # Default value
        for runner in self.RUNNERS: 
            if runner.first_name == old_FN and runner.last_name == old_LN:
                runner.first_name = new_FN
                runner.last_name = new_LN
                runner_was_found = True
                print(f"The name of the runner {old_FN} {old_LN} was changed to {new_FN} {new}_LN")
        if not runner_was_found: 
            print(f"Runner {old_FN} {old_LN} could not be found in current session!")
    
    def changeNumLaps(self, R_FN, R_LN, NumLaps):
        runner_was_found = False

        for runner in self.RUNNERS:
            if runner.first_name == R_FN and runner.last_name == R_LN:
                runner_was_found = True
                runner.number_of_laps = NumLaps
                print("The value was changed!")

        if not runner_was_found:
            print(f"The runner {R_FN} {R_LN} could not be found!") 

    def changeSponsorship(self, R_FN, R_LN, S_FN, S_LN, value_per_lap, maxval):
        runner_was_found = False
        sponsorship_was_found = False
        for runner in self.RUNNERS:
            if runner.first_name == R_FN and runner.las_name == R_LN: 
                runner_was_found = True
                for sponsorship in runner.sponsor_list:
                    if sponsorship[0].first_name == S_FN and sponsorship[0].last_name == S_LN: 
                        sponsorship_was_found = True
                        sponsorship[1] = value_per_lap
                        sponsorship[2] = maxval
        if not runner_was_found: 
            print(f"The runner {R_FN} {R_LN} could not be found!")
            return None
        
        if not sponsor_was_found:
            print(f"The sponsor {S_FN} {S_LN} could not be found!") 
    
    def getRunnerInfo(self, runner_first_name, runner_last_name):
        runner_was_found = False

        for runner in self.RUNNERS: 
            if runner.first_name == runner_first_name and runner.first_name == runner_first_name: 
                runner_was_found = True
                print("-----------RUNNER INFO-----------")
                print(f"Name: {runner.first_name} {runner.last_name}") 
                print(f"Value per lap: {runner.value_per_lap}")
                print(f"Number of laps: {runner.number_of_laps}") 
                print(f"Collected in total: {runner.collected_in_total}")
                print("----------------------------------") 
                break
        if not runner_was_found: 
            print("The runner {runner_first_name} {runner_last_name} could not be found!") 

    def getSponsorInfo(self): 
        pass

    def saveSession(self):
        self.SPONSORS = updateSponsorList(self.RUNNERS)
        encodeToJSON(self.session_name, self.RUNNERS, self.SPONSORS)

if __name__ == '__main__':
    # THIS IS A PORTION OF THE CODE THAT IS USED TO TEST DIFFERENT SEQUENCES OF 
    # FUNCTION CALLS...
    session = Session("testsession") 
    session.addRunner("Axel", "Lundin")
    session.addRunner("Simon", "Frisk")
    session.addSponsorship("Simon", "Frisk", "Axel", "Lundin", 20, 1000)
    session.addSponsorship("Axel", "Lundin", "Lars", "Lundin", 10, 100)
    session.addSponsorship("Simon", "Frisk", "Vivianne", "Manlai", 20, 40)

    encodeToJSON(session.session_name, session.RUNNERS, session.SPONSORS)
