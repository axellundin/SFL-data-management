import sponsor

class Runner():
    ''' '''
    def __init__(self, first_name, last_name, number_of_laps=0):
        self.first_name = first_name
        self.last_name = last_name
        self.sponsor_list = []
        self.number_of_laps = number_of_laps
        self.value_per_lap = 0
        self.collected_in_total = 0

    def addSponsorship(self, sponsor_first_name, sponsor_last_name, value_per_lap, maximum):
        
        # Instanstiate the sponsor object and make sure that it
        # doesn't already exist in the JSON file.
        
        '''CODE TO READ THE JSON AND GIVE BACK 'EXISTS:TRUE?FALSE' GOES HERE'''

        # For now: define
        exists = False
        
        if exists==False:
            NEW_SPONSOR = sponsor.Sponsor(sponsor_first_name, sponsor_last_name) 
            # Create a sponsorship object that consists of the connection to the sponsors name and that includes the value that the sponsor has decided to sponsor the runner with
            SPONSORSHIP = [NEW_SPONSOR, value_per_lap, maximum] 
            self.sponsor_list.append(SPONSORSHIP)
        else:
            # CODE TO ADD RUNNER TO JSON GOES HERE
            pass
        
        self.updateJSON()

    def removeSponsorship(self, sponsor_first_name, sponsor_last_name):
        ''' This is a function that removes a sponsor from the list of sponsors '''
        # Search through the list of sponsors that is attributed to the runner
        # and remove any element with the same name. The status will be reported to the terminal.
        # If the name could not be found, a descriptive message will be displayed. 

        for sponsorship in self.sponsor_list:
            if sponsorship[1].first_name == sponsor_first_name and sponsorship[1].last_name == sponsor_last_name: 
                self.sponsor_list.remove(sponsorship)  
                print(f"The sponsorship of {self.first_name} {self.lastname} by {sponsor_first_name} {sponsor_last_name} has been removed!")
                break

        print(f"An entry with the name {sponsor_first_name} {sponsor_last_name} could not be found among the sponsorships!")
        
        self.updateJSON()

    def changeSponsorInfo(self, sponsor_first_name, sponsor_last_name, value_per_lap, maximum):
        # CODE TO CHANGE THE JSON FILE GOES HERE
        pass

    def updateJSON(self):
       # Code that updates the JSON file goes here
       pass
