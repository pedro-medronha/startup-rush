from typing import List
from models.startup import Startup
from models.battle import Battle

class Rush:
    
    def __init__(self):
        self.startups: List[Startup] = [] # List of startups
        self.current_round = 1
        self.battles: List[Battle] = [] # List of battles