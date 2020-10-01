

class Sponsor():
    ''' This is a class for a sponsor object. The parameters that are
    passed to the constructor are connected to the name of the sponsor.'''
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.TO_PAY = 0
        self.HAS_TAKEN_PART = False
