from models.startup import Startup

class Battle:
    
    def __init__(self, startup1: Startup, startup2: Startup):
        self.startup1 = startup1
        self.startup2 = startup2
        self.ended = False