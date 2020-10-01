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
                "maxval": sponsor[1], 
                "topay": sponsor[2]
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
    print(names_that_exist)
    
    number_of_copys=0

    while session_name in names_that_exist:
        number_of_copys+=1
        if number_of_copys>1:
            session_name = session_name[:len(session_name) - len(str(number_of_copys-1))] + (str) (number_of_copys)
        else: 
            session_name = session_name +(str) (number_of_copys)
    print(sessionsdir + session_name)
    
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


def readFromJSON(session_name):
    pass

class Session():
    ''' This is a class that holds information about a complete session of the 
    SPRING FÖR LIVET event. The class variables include the list of runners with their
    respective information, as well as a list of sponsors with relevant connections to 
    the runners. '''

    def __init__(self, session_name, MODE='REGULAR'):
        
        self.session_name = session_name

        if MODE=='REGULAR':
            # SPONSORS INIT
            self.SPONSORS = []
            
            # RUNNERS INIT
            self.RUNNERS = []
        elif MODE=='READ':
            while True:
                session_name = input("Please enter the name of the session that you would like to enter:\n")

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
                print("The sponsorship was added!")
                return None
        print("The sponsorship could not be found!")

if __name__ == '__main__':
    session = Session("testsession") 
    session.addRunner("Axel", "Lundin")
    session.addRunner("Simon", "Frisk")
    session.addSponsorship("Simon", "Frisk", "Axel", "Lundin", 20, 1000)
    session.addSponsorship("Axel", "Lundin", "Lars", "Lundin", 10, 100)
    session.addSponsorship("Simon", "Frisk", "Vivianne", "Manlai", 20, 40)

    encodeToJSON(session.session_name, session.RUNNERS, session.SPONSORS)
