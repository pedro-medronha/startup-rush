from typing import List
from models.startup import Startup

class Battle:
    
    def __init__(self, startup1: Startup, startup2: Startup, round: int):
        self.startup1 = startup1
        self.startup2 = startup2
        self.round = round
        self.applied_events: List[str] = [] #eventos que foram aplicados na batalha
        self.winner: Startup = None
        self.ended = False
        
    def __str__(self):
        return f"Battle between {self.startup1.name} and {self.startup2.name} in round {self.round}."