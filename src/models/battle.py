from typing import List
from models.startup import Startup

class Battle:
    
    def __init__(self, startup1: Startup, startup2: Startup, round_number: int):
        self.startup1 = startup1
        self.startup2 = startup2
        self.round_number = round_number
        self.applied_events_startup1: List[str] = [] #eventos aplicados à startup1
        self.applied_events_startup2: List[str] = [] #eventos aplicados à startup2
        self.winner = None
        self.ended = False
        
    def __str__(self):
        if self.startup2 is None:
            return f"{self.startup1.name} (BYE)"
        return f"{self.startup1.name} vs {self.startup2.name}"